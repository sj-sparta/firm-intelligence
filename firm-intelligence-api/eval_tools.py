"""
Small, pure helpers for scoring. No network and no model.
"""


import re

from grounding import is_refusal, normalise # one definition of refusal

def contains_evidence(chunk_text: str, evidence: str) -> bool:
    """True if the chunk holds the whole evidence span. Line breaks never break a match"""
    return normalise(evidence) in normalise(chunk_text)


# alternative_matches
def _alternative_matches(answer: str, alternative: str) -> bool:
    prefix = alternative.endswith("*")
    core = re.escape(alternative.rstrip("*").lower())
    ending = "" if prefix else r"(?![a-z0-9])"
    return re.search(rf"(?<![a-z0-9]){core}{ending}", answer.lower()) is not None


# keywords_present
# what the keywords list looks like
# Question                            keywords                   meaning
# q11 (offshore wind capacity)        ["4.2"]                   Must mention 4.2
# q14 (Okonkwo Bell offices)          ["Lagos", "Nairobi"]     Must mention both
def keywords_present(answer: str | None, keywords: list[str]) -> bool:
    """True only for a non-refusal answer that contains every keyword group"""
    if is_refusal(answer):
        return False
    return all(
        any(_alternative_matches(answer, alt) for alt in group.split("|")) for group in keywords
    )

# Answer                                 # Result
# Offices in Lagos and Nairobi          True
# An office in Lagos                   False
# An office in Nairobi                 False 