"""
Same evidence, same questions, 2 system prompts.
Outcome: what does the looser system prompt do???
"""


import grounding
import llm
from corpus import CORPUS_DOCUMENTS


LOOSE_PROMPT = (
    "You are a helpful legal market analyst. Answer the question as fully and helpfully as "
    "you can. Cite the document id in square brackets where you use it."
)

QUESTIONS = [
    "Who is the managing partner of Harding & Voss, and how long have they held the role?",
    "How does Harding & Voss's profitability compare with the Magic Circle firms?",
]


def main() -> None:
    doc = next(d for d in CORPUS_DOCUMENTS if d["id"] == "doc-101")
    context = f"[{doc['id']}] {doc['title']}\n{doc['body']}"

    # two loops, 4 model calls
        # q1, loose
        # q1, grounded
        # q2, loose
        # q2, grounded

    for question in QUESTIONS:
        print("=" * 50)
        print("QUESTION: ", question)

        for name, prompt in [("loose", LOOSE_PROMPT), ("grounded", llm.GROUNDED_SYSTEM_PROMPT)]:
            result = llm.answer_from_context(question, context, system=prompt)
            report = grounding.check_citations(result["answer"], [doc["id"]])

            print(f"\nn-- {name} prompt ---")
            print(result["answer"])
            print(f"\n  refusal: {report['refusal']} passed: {report['passed']}")
            for sentence in report["uncited_sentences"]:
                print(f"  UNCITED: {sentence}")



if __name__ == "__main__":
    main()