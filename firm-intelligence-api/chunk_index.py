"""
One Chroma collection per chunking strategy.... so that strategies can be compared side by side

Each colection remembers a "fingerprint" of the chunks and the embedding model that built it.
If either changes , the collection is rebuilt from scratch.
"""

# things to note from our switch to Chroma

# embed_texts is imported not rewritten... embedding provider hasn't changed... only the storage has
# configuration=.... -> not optional, we are choosing something different from Chromas default
# Chroma retuirn distance, we return similarity
    # in Chroma, lower is better
    # higher was better for ours.... (1 - distance) converts
# upsert instead of add -> add fails on an id that already exists, upsert overwrites

import hashlib
import chromadb

import chunking
import knowledge
from corpus import CORPUS_DOCUMENTS
from documents import DOCUMENTS

ALL_DOCUMENTS = DOCUMENTS + CORPUS_DOCUMENTS
BATCH_SIZE = 128 # Voyage's own guidance: batch documents to stay well inside rate limits

chroma = chromadb.PersistentClient(path="./chroma_store")


def collection_name(strategy: str) -> str:
    return f"chunks_{strategy}"


def collection_for(strategy: str):
    return chroma.get_or_create_collection(
        name=collection_name(strategy), configuration={"hnsw": {"space": "cosine"}}
    )


def embed_batched(texts: list[str], input_type: str) -> tuple[list[list[float]], int]:
    """Embed any number of texts in batches. Return all vectors and the total token count."""
    vectors: list[list[float]] = []
    tokens = 0

    for start in range(0, len(texts), BATCH_SIZE):
        batch_vectors, batch_tokens = knowledge.embed_texts(texts[start:start + BATCH_SIZE], input_type=input_type)
        vectors.extend(batch_vectors)
        tokens += batch_tokens
    return vectors, tokens


# the fingerprint changes if the text, the model or the order changes... and stays put of nothing does
def fingerprint(chunks: list[dict]) -> str:
    # SHA-256 - a recipe that turns any text into a fixed-length code (64 chars)
    digest = hashlib.sha256(knowledge.EMBED_MODEL.encode())
    for c in chunks:
        digest.update(f"{c['id']}\n{c['text']}\n".encode())
    return digest.hexdigest()[:16]



def build(strategy: str, force: bool = False) -> dict:
    """Make sure the strategy's collection matches the current corpus, chunker and model."""
    """Answers one q.... is the index I already have still correct?"""
    # pt1
    chunks = chunking.chunk_corpus(ALL_DOCUMENTS, strategy)
    fp = fingerprint(chunks)
    col = collection_for(strategy)
    stored = col.get(limit=1, include=["metadatas"])["metadatas"]
    if not force and col.count() == len(chunks) and stored and stored[0].get("fingerprint") == fp:
        return {"strategy": strategy, "chunks": len(chunks), "embedding_tokens": 0, "rebuilt": False}

    #pt2 - the rebuild
    try:
        chroma.delete_collection(collection_name(strategy))
    except Exception:
        pass

    col = collection_for(strategy)
    vectors, tokens = embed_batched([c["text"] for c in chunks], input_type="document")
    col.upsert(
        ids=[c["id"] for c in chunks],
        embeddings=vectors,
        documents=[c["text"] for c in chunks],
        metadatas=[{"doc_id": c["doc_id"], "title": c["title"], "fingerprint": fp} for c in chunks],
    )
    return {"strategy": strategy, "chunks": len(chunks), "embedding_tokens": tokens, "rebuilt": True}


# CURRENT - 

# NEW FUNCTIONS ADDS - search_with_vectors
# the read side
# it takes question vectors that are already embedded, so questions are embedded once and reused across all 6 categories

def search_with_vectors(strategy: str, query_vectors: list[list[float]], k: int) -> list[list[dict]]:
    """Ranked hits for every query vector. Takes vectors, so questions are embedded only once."""
    col = collection_for(strategy)
    if col.count() == 0:
        raise RuntimeError(f"Index for '{strategy}' is empty, build it first")
    n_results = min(k, col.count())
    ranked = []
    for vector in query_vectors:                     # one question at a time
        result = col.query(query_embeddings=[vector], n_results=n_results)
        ranked.append([
            {"id": meta["doc_id"], "chunk_id": chunk_id, "title": meta["title"],
             "text": text, "score": 1 - distance}
            for chunk_id, text, meta, distance in zip(
                result["ids"][0], result["documents"][0], result["metadatas"][0], result["distances"][0])
        ])
    return ranked











"""
a chunk that only keyword search found has no cosine score.... our relevance gate needs one
"""

def cosine_for(strategy: str, query_vector: list[float], chunk_ids: list[str]) -> dict[str, float]:
    if not chunk_ids:
        return {}

    stored = collection_for(strategy).get(ids=chunk_ids, include=["embeddings"])

    return {
        chunk_id: float(knowledge.cosine_similarity(query_vector, list(vector)))
        for chunk_id, vector in zip(stored["ids"], stored["embeddings"])
    }


# where it fits in hybrid.py
    # vector search returns its top 10 with a cosine
    # keyword search returns its top 10
    # RRF merges them
    # any chunk in the keyword list but NOT in the vector list is passed to "cosine_for"
    # now every hit has a cosine... so the gate works the same on all of them
        # score >= 0.45 orrrr exact_match

# question mentions 3307
# chunk mentions 3307














