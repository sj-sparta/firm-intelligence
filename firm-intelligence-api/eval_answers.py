"""
Answer quality for the strategies your shortlist... this file will call the model.

Cost: one model call per question per strategy.... 32 q's.... 3 chunks of context each
Print results to a file.... aval_results/answer.json.
"""

import argparse
import json
import statistics
from pathlib import Path

import chunk_index
import context
import llm
from eval_set import EVAL_SET
from eval_tools import keywords_present
from grounding import is_refusal


def run(strategy: str, vectors: list[list[float]], floor: float) -> dict:
    # top 3 chunks for every question
    ranked = chunk_index.search_with_vectors(strategy, vectors, k=3)
    # place to store results
    correct, false_refusals, wrong, tokens = [], [], [], []
    for q, hits in zip(EVAL_SET, ranked):
        usable = [h for h in hits if h["score"] >= floor]
        # passes gate - build the context and ask model
        # not pass - refuse without calling model (like /knowledge/ask
        if usable: 
            result = llm.answer_from_context(q["question"], context.build_context(usable))
            answer = result["answer"]
            tokens.append(result["input_tokens"])
        else:
            answer = None

        # was the result right???
            # answerable - right if the answer contains the expected keywords (None contains nothing... so a refusal counts as wrong)
            # unanswerable - right if its refused 
        ok = keywords_present(answer, q["keywords"]) if q["doc_id"] else is_refusal(answer)
        correct.append((q, ok))
        if not ok:
            (false_refusals if q["doc_id"] and is_refusal(answer) else wrong).append(q["id"])

    answerable = [ok for q, ok in correct if q["doc_id"]]
    unanswerable = [ok for q, ok in correct if not q["doc_id"]]

    return {
        "answer_accuracy": round(statistics.mean(answerable), 3),
        "refusal_accuracy": round(statistics.mean(unanswerable), 3),
        "false_refusals": false_refusals,
        "wrong_or_unrefused": wrong,
        "model_calls": len(tokens),
        "avg_input_tokens": round(statistics.mean(tokens)) if tokens else 0,
    }




def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("strategies", nargs="+")
    parser.add_argument("--floor", type=float, default=0.35)
    args = parser.parse_args()

    for strategy in args.strategies:
        chunk_index.build(strategy)
    vectors, _ = chunk_index.embed_batched([q["question"] for q in EVAL_SET], input_type="query")

    results = {s: run(s, vectors, args.floor) for s in args.strategies}
    print(f"floor = {args.floor}\n")
    print(f"{'strategy':<22}{'answers':>9}{'refusals':>10}{'calls':>7}{'avg in tokens':>15}")
    for s, r in results.items():
        print(f"{s:<22}{r['answer_accuracy']:>9.2f}{r['refusal_accuracy']:>10.2f}"
              f"{r['model_calls']:>7}{r['avg_input_tokens']:>15}")
        print(f"    false refusals: {', '.join(r['false_refusals']) or 'none'}")
        print(f"    wrong or not refused: {', '.join(r['wrong_or_unrefused']) or 'none'}")

    Path("eval_results").mkdir(exist_ok=True)
    Path("eval_results/answers.json").write_text(json.dumps({"floor": args.floor, **results}, indent=2))


if __name__ == "__main__":
    main()




