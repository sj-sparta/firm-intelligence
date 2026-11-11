"""
The relevance gate - does a retrieved chunk deserve to reach the model?

Each hit is judged on the score it was ranked by
    - a hit from Azure carries 'rerank_score' (0-4, from the semnatic reranker)
    - a hit from the local index carries only a cosine similarity in 'score'
A hit holding the same number/identifier as the question (exact_match) always passes.
"""


def is_usable(hit: dict, cosine_floor: float, rerank_floor: float) -> bool:
    if hit.get("exact_match", False):
        return True
    if hit.get("reranker_score") is not None:
        return hit["rerank_score"] >= rerank_floor
    return hit["score"] >= cosine_floor