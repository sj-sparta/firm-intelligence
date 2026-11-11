""""
How retrieved hits become the text the model reads
Failure: lost in the middle
"""

# hits
def order_for_context(hits: list[dict]) -> list[dict]:
    """Best hit first, second best last, weakest in the middle.
    Ranked [a, b, c, d, e] becomes [a, c, e, d, b].
    """
    ranked = sorted(hits, key=lambda h: h["score"], reverse=True)
    front = ranked[0::2]          # a, c, e
    back = ranked[1::2]           # b, d
    return front + back[::-1]     # a, c, e, d, b

def build_context(hits: list[dict]) -> str:
    """The exact text block the model sees, one labelled section per hit."""
    return "\n\n".join(f"[{h['id']}] {h['title']}\n{h['text']}" for h in order_for_context(hits))