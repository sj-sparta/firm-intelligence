"""
Rank fusion - merge ranked lists into one
"""

def reciprocal_rank_fusion(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for position, item in enumerate(ranking, start=1):
            scores[item] = scores.get(item, 0.0) + 1.0 / (k + position)
    # ties keep the order the ids were added
    return sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
    # each judge gives a card 1 / (k + position) points... position 1 is the top of thats judges list.
        # with the standard k = 60
            # position                points
            # 1st                     1/61 = ...
            # 2nd                     1/62 = ...
            # 3rd                     1/63 = ...