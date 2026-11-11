"""
Azure AI Search bvackend.... this is going to do the same job as knowledge_store (count, build_index, search).

On search call does 3 things:
1. keyword search (BM25) and vector search run together, and Azure fuses them with RRF
2. the semantic reranker rereads the top results beside the question and scores each 0 to 4
3. the hits come back best first, carrying that score for the relevance gate (gate.py)
"""


import time
from functools import lru_cache

from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.models import VectorizedQuery

import azure_index
import bm25
import chunk_index
import settings

# semantic ranker only ever reads the top 50 results, so we'll ask for that many and trim to top_k afterwards
CANDIDATES = 50

# chunks per upload request
BATCH = 100

NOT_BUILT = "The Azure index is empty or missing. Build it with: python -m azure_build"



# pt2 - signing in and the two clients

@lru_cache(maxsize=None)
def _credential() -> DefaultAzureCredential:
    """Signs in as you after 'az login', or as the managed identity once deployed"""
    return DefaultAzureCredential()

def _endpoint() -> str:
    if not settings.AZURE_SEARCH_ENDPOINT:
        raise RuntimeError("AZURE_SEARCH_ENDPOINT is not set. "
                           "Example: export AZURE_SEARCH_ENDPOINT=https://<your-service>.search.windows.net")
    return settings.AZURE_SEARCH_ENDPOINT

@lru_cache(maxsize=None)
def search_client() -> SearchClient:
    return SearchClient(endpoint=_endpoint(), index_name=settings.AZURE_SEARCH_INDEX, credential=_credential())


@lru_cache(maxsize=None)
def index_client() -> SearchIndexClient:
    return SearchIndexClient(endpoint=_endpoint(), credential=_credential())



def _identifiers(text: str) -> set[str]:
    """Tokens containing a digit (e.g. 3307), same as in hybrid.py"""
    return {token for token in bm25.tokenize(text) if any(ch.isdigit() for ch in token)}


def count() -> int:
    """Number of chunks in Azure index, 0 if it does not exist.
        - Needs only the query permission.
    """
    try:
        return search_client().search(search_text="*", include_total_count=True, top=0).get_count()
    except ResourceNotFoundError:
        return 0


# search with vector 
# get every chunk from its Voyage vector
# make new documents searachable
# drop and recreate index

def search_with_vector(question: str, query_vector: list[float], top_k: int = 3, semantic: bool=True) -> list[dict]:
    # clean the question
        # What is "LP-3307"?
        # what is lp 3307
    search_text = " ".join(bm25.tokenize(question)) or "*"

    # build one query that will do 2 searches
        # keyword half and vector half
    options = {
        "search_text": search_text,
        "vector_queries": [VectorizedQuery(vector=query_vector, k_nearest_neighbors=CANDIDATES, fields="embedding")],
        "select": ["chunk_id", "doc_id", "title", "text"],
        "top": max(top_k, CANDIDATES),
    }
    # switch on the semantic reranker
    if semantic:
        options["query_type"] = "semantic"
        options["semantic_configuration_name"] = settings.SEMANTIC_CONFIG

    # run it, trim it, and if needed handle any missing index
    try:
        results = list(search_client().search(**options))[:top_k]
    except ResourceNotFoundError as error:
        raise RuntimeError(NOT_BUILT) from error
    if not results:
        raise RuntimeError(NOT_BUILT)

    # turn each result into a hit  
    # 2 scores: rerankers score (0 - 4), and the fused rank score from the merge
    wanted = _identifiers(question) if settings.EXACT_MATCH_RULE else set()
    hits = []
    for result in results:
        rerank = result.get("@search.reranker_score")
        fused = result["@search.score"]

        hits.append({
            "id": result["doc_id"],
            "chunk_id": result["chunk_id"],
            "title": result["title"],
            "text": result["text"],
            "score": rerank if rerank is not None else fused,
            "rerank_score": rerank,
            "rrf": round(fused, 5),
            "exact_match": bool(wanted & set(bm25.tokenize(result["text"]))),
        }) 
    return hits


def _local_chunks(strategy: str) -> list[dict]:
    """
    Every chunk with its Voyage vector
    Reusing the vectors costs no embedding tokens (also means Azure has the exact same chunks and vectors as the local search)
    """
    chunk_index.build(strategy) # free when up to date
    # stored is a dict of parallel lists
        # stored["ids"], stored["embeddings"]....
    stored = chunk_index.collection_for(strategy).get(include=["embeddings", "documents", "metadatas"])
    # walk all 4 lists together
    return [
        {
            "chunk_key": azure_index.key_for(chunk_id),
            "chunk_id": chunk_id,
            "doc_id": meta["doc_id"],
            "title": meta["title"],
            "text": text,
            "embedding": [float(number) for number in vector],
        }
        for chunk_id, vector, text, meta in zip(stored["ids"], stored["embeddings"], stored["documents"], stored["metadatas"])
    ]


def _wait_until_counted(expected: int, seconds:int = 30) -> None:
    """
    New documents become searchable a moment after upload, so we wait for the count to catchup
    """
    deadline = time.time() + seconds
    while time.time() < deadline:
        if count() >= expected:
            return
        time.sleep(1)
    raise RuntimeError(f"Uploaded {expected} chunks, but the index reports {count()} after {seconds} seconds")


def build_index(strategy: str) -> int:
    """
    Drop and recreate the Azure index... then load every chunk.... return chunk count
    """
    docs = _local_chunks(strategy)
    keys = [doc["chunk_key"] for doc in docs]
    if len(set(keys)) != len(keys):
        # the ids of doc-1#01 and doc-1_01 would both become doc-1_01
        raise RuntimeError("Two chunk ids turn into the same Azure key, so chunks would overwrite each other")
    # check the vector sizes
    bad = [doc for doc in docs if len(doc["embedding"]) != azure_index.DIMENSIONS]
    if bad:
        raise RuntimeError(f"{bad[0]['chunk_id']} has {len(bad[0]['embedding'])} numbers per vector, but the index expects {azure_index.DIMENSIONS}. Did the embedding model change?")

    name = settings.AZURE_SEARCH_INDEX
    try:
        index_client().delete_index(name)
    except ResourceNotFoundError:
        pass
    index_client().create_index(azure_index.index_definition(name))

    for start in range(0, len(docs), BATCH):
        results = search_client().upload_documents(documents=docs[start:start + BATCH])
        failed = [result for result in results if not result.succeeded]
        if failed:
            raise RuntimeError(f"Azure rejected {len(failed)} chunks. First: {failed[0].key}: {failed[0].error_message}")

    # wait, then report
    _wait_until_counted(len(docs))
    return len(docs)