"""
Does the model miss a fact buried in the middle of long context?
Cost: positions x trials model calls... the defaults make 15 calls of roughly 6,000 input tokens
"""


import argparse
import random
import re

import llm
from corpus import CORPUS_DOCUMENTS
from documents import DOCUMENTS

# the needle - fact that appears nowhere else and contradicts nothing in the corpus
NEEDLE = {
    "id": "doc-900",
    "title": "Okonkwo Bell: Knowledge Team Update",
    "text": "The Okonkwo Bell knowledge team catalogued 1,742 precedent documents during its summer review."
}
QUESTION = "How many precedent documents did the Okonkwo Bell knowledeg team catalogue in its summer review?"
POSITIONS = [0.0, 0.25, 0.5, 0.75, 1.0]


# distractors - builds the "haystack" material
def distractors() -> list[dict]:
    blocks = []
    # go through all 16 doc (8 + 8)
    for doc in DOCUMENTS + CORPUS_DOCUMENTS:
        sections = re.split(r"(?m)^## ", doc["body"]) if "## " in doc["body"] else [doc["body"]]
        for section in sections:
            heading, _, text = section.partition("\n") if "## " in doc["body"] else ("", "", section)
            if text.strip():
                title = f"{doc['title']} / {heading.strip()}" if heading.strip() else doc["title"]
                blocks.append({"id": doc["id"], "title": title, "text": text.strip()})

    return blocks


# haystack - this will allow us to place our "needle" inside our haystack
def haystack(blocks: list[dict], position: float, seed: int) -> str:
    """Shuffle the distractors, then insert the needle at the requested position"""
    items = blocks[:]
    random.Random(seed).shuffle(items)
    items.insert(round(position * len(items)), NEEDLE)
    # when position is 0, index is 0, result is (N = needle) N 3 2 1 5 4
    # when position is 1.00, index is 5, result is (N = needle)  3 2 1 5 4 N
    return "\n\n".join(f"[{b['id']}] {b['title']}\n{b['text']}" for b in items)



# found
def found(answer: str) -> bool:
    # match 1742 and 1,742
    return re.search(r"1,?742", answer) is not None


def main() -> None:
    blocks = distractors()
    for position in POSITIONS:
        answers = [llm.answer_from_context(QUESTION, haystack(blocks, position, seed=t))["answer"] for t in range(3)]
        print(position, sum(found(a) for a in answers), "/ 3")

if __name__ == "__main__":
    main()