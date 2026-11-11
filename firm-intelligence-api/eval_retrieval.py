"""
The step builds the scoreboard.
Score every chunking strategy against the eval set.

build all 6 indes -> embed the 32 questions once -> search every index -> score -> print + save
"""

import json
import statistics
from pathlib import Path 

import chunk_index
import chunking
from  eval_set import EVAL_SET
from eval_tools import contains_evidence

# look at the top 1, top 3 and the top 5 results
K_VALUES = (1, 3, 5)


# where is the right chunk?
def first_hit_rank(hits: list[dict], evidence: str) -> int | None:
    for rank, hit in enumerate(hits, start=1):
        if contains_evidence(hit["text"], evidence):
            return rank
    return None


# turn our results into numbers
# find the rank of the correct chunk for every answerable question.... then turn those ranks into scores
def score_strategy(questions: list[dict], ranked: list[list[dict]]) -> dict:
    """Recall@k, MRR, context size and the questions thats missed, for ONE strategy."""
    answerable = [(q, hits) for q, hits in zip(questions, ranked) if q["doc_id"]]
    unanswerable = [(q, hits) for q, hits in zip(questions, ranked) if not q["doc_id"]]
    ranks = [first_hit_rank(hits, q["evidence"]) for q, hits in answerable]

    # group by question kind
    kinds: dict[str, list[bool]] = {}
    for (q, _), rank in zip(answerable, ranks):
        kinds.setdefault(q["kind"], []).append(rank is not None and rank <= 3)

    return {
        **{f"recall@{k}": round(statistics.mean(r is not None and r <= k for r in ranks), 3) for k in K_VALUES},
        "mrr": round(statistics.mean(1 / r if r else 0 for r in ranks), 3),
        "context_words@3": round(statistics.mean(
            sum(len(h["text"].split()) for h in hits[:3]) for _, hits in answerable)),
        # our confidence scores
            # we use the gap between them to choose our relevance floor
        "top_score_answerable": round(statistics.mean(hits[0]["score"] for _, hits in answerable), 3),
        "top_score_unanswerable": round(statistics.mean(hits[0]["score"] for _, hits in unanswerable), 3),
        "recall@3_by_kind": {kind: round(statistics.mean(v), 2) for kind, v in sorted(kinds.items())},
        "missed@3": [q["id"] for (q, _), r in zip(answerable, ranks) if not r or r > 3],
    }




def main() -> None:
    print("Building indexes (free if nothing has changed)...")
    for strategy in chunking.STRATEGIES:
        b = chunk_index.build(strategy)
        print(f"  {strategy:<22} {b['chunks']:>3} chunks  "
              f"{'rebuilt' if b['rebuilt'] else 'up to date':<10}  {b['embedding_tokens']:>6} tokens")

    vectors, tokens = chunk_index.embed_batched([q["question"] for q in EVAL_SET], input_type="query")
    print(f"\nEmbedded {len(EVAL_SET)} questions once ({tokens} tokens), reused for every strategy.\n")

    results = {}
    for strategy in chunking.STRATEGIES:
        ranked = chunk_index.search_with_vectors(strategy, vectors, k=max(K_VALUES))
        results[strategy] = score_strategy(EVAL_SET, ranked)

    header = f"{'strategy':<22}{'R@1':>6}{'R@3':>6}{'R@5':>6}{'MRR':>7}{'ctx words':>11}{'top ans':>9}{'top unans':>11}"
    print(header)
    print("-" * len(header))
    for strategy, r in results.items():
        print(f"{strategy:<22}{r['recall@1']:>6.2f}{r['recall@3']:>6.2f}{r['recall@5']:>6.2f}"
              f"{r['mrr']:>7.2f}{r['context_words@3']:>11}{r['top_score_answerable']:>9.2f}"
              f"{r['top_score_unanswerable']:>11.2f}")
    print("\nMissed at k=3:")
    for strategy, r in results.items():
        print(f"  {strategy:<22} {', '.join(r['missed@3']) or 'none'}")

    Path("eval_results").mkdir(exist_ok=True)
    Path("eval_results/retrieval.json").write_text(json.dumps(results, indent=2))
    print("\nSaved eval_results/retrieval.json")


if __name__ == "__main__":
    main()