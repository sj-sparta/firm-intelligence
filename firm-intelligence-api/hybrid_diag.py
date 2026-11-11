"""Show where hybrid search loses its results. One Voyage call. Delete when done."""
import bm25, chunk_index, fusion, hybrid, knowledge, knowledge_store

S = knowledge_store.CHUNK_STRATEGY
Q = "What is lp 3307 about?"
vectors, _ = knowledge.embed_texts([Q], input_type="query")

print("1. chunks in the local index:", chunk_index.collection_for(S).count())
vector_hits = chunk_index.search_with_vectors(S, [vectors[0]], k=10)[0]
print("2. vector search returned:", len(vector_hits), [h["chunk_id"] for h in vector_hits][:3])
keyword_hits = hybrid.keyword_index(S).search(Q, k=10)
print("3. keyword search returned:", len(keyword_hits), [h["chunk"]["id"] for h in keyword_hits][:3])
fused = fusion.reciprocal_rank_fusion([[h["chunk_id"] for h in vector_hits],
                                       [h["chunk"]["id"] for h in keyword_hits]])
print("4. fusion returned:", len(fused), [(i, round(s, 5)) for i, s in fused[:3]])
final = hybrid.search_with_vector(S, Q, vectors[0], top_k=3)
print("5. hybrid.search_with_vector returned:", len(final), [h["chunk_id"] for h in final])
print("6. SEARCH_MODE:", knowledge_store.SEARCH_MODE)
