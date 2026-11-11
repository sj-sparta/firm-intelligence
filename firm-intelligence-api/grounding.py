"""Checks on generated answers. Pure functions: no network, no model, no FastAPI

Failure - ungrounded hallucination: sentences that carry no citation at all.
Failure - citation drift: citations that point at the wrong source, or at no source.

"""

import re
REFUSAL_SENTENCE = "The provided documents do not answer that question."

# the findall will return doc-001, rather than [doc-001]
CITATION = re.compile(r"\[(doc-\d{3})\]")


# normalise - lower-case and sqiash every run of spaces, tabs/newlines into one space
    # we need this as models sometimes wrap lines... so without normalise a refusal 
    # split across two lines would not match
def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()

# is_refusal - treats None as a refusal too.
    # we are standardising the refusal
    # /knowledge/ask returns answer: None when it refuses before calling the model, and the check should agree with the endpoint
def is_refusal(answer: str | None) -> bool:
    return answer is None or normalise(REFUSAL_SENTENCE) in normalise(answer)



def split_sentences(text: str) -> list[str]:
    """Split an answer into sentences, keeping a trailing citation with its sentence.

    Models can write both "Revenue rose [doc-101]." and "Revenue rose. [doc-101]".
    The second form would otherwise leave "[doc-101]" as a sentence of it own.
    """

    pieces = []
    for line in text.splitlines():
        line = line.strip(" -*\t")
        if line:
            pieces.extend(p for p in re.split(r"(?<=[.!?])\s+", line) if p)

    sentences: list[str] = []
    for piece in pieces:
        if sentences and CITATION.sub("", piece).strip(" .") ==  "":
            sentences[-1] = f"{sentences[-1]} {piece}"
        else:
            sentences.append(piece)
    return sentences


# citations_in
def citations_in(text: str) -> list[str]:
    return CITATION.findall(text)

# check_citations
def check_citations(answer: str | None, source_ids: list[str]) -> dict:
    """Cheap structural checks. Catches uncited claims and citations to sources we never gave.
    """
    if is_refusal(answer):
        return {"refusal": True, "cited": [], "invalid": [], "uncited_sentences": [], "passed": True}

    sentences = split_sentences(answer)
    cited = sorted(set(citations_in(answer)))
    invalid = [doc_id for doc_id in cited if doc_id not in source_ids]
    # Very short sentences ("Yes." or "In Summary:") are claims not worth policing
    uncited = [s for s in sentences if not CITATION.search(s) and len(s.split()) >= 3]

    return {
        "refusal": False,
        "cited": cited,
        "invalid": invalid,
        "uncited_sentences": uncited,
        "passed": not invalid and not uncited
    }



