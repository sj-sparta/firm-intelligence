"""
BM25 keyword search... we'll build by hand first so we can see every term in the score

No network, no model calls
It will index the same chunks the vector index holds.... so our 2 retrievers can be fused chunk for chunk.
"""

import math
import re
from collections import Counter

K1 = 1.5   # how quickly repeating a word stops adding score
B = 0.75   # how strongly long chunks are marked down

# tokenize - lowercase words and numbers
    # "LP-3307" becomes ["lp", "3307"]
    # "What is lp 3307 about?" becomes ["what", "is", "lp", "3307", "about"]
    # walkthrough
        # what, is and about appear in many chunks.... so they add very little
        # 3307 appears in one chunk, the Tokyo one, so it will carry the highest rarity 
            # most of that chunks winning score comes from the rare tokens it shares with the question
def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())

# BM25 class
    # idf
    # score
    # search

class BM25Index:
    def __init__(self, chunks: list[dict]):
        if not chunks:
            raise ValueError("cannot build a keyword index from zero chunks")
        # count everything upfront
        self.chunks = chunks
        self.term_counts = [Counter(tokenize(c["text"])) for c in chunks]
        self.lengths = [sum(counts.values()) for counts in self.term_counts]
        self.avg_length = sum(self.lengths) / len(chunks)

        self.doc_freq = Counter()
        for counts in self.term_counts:
            self.doc_freq.update(counts.keys())

    def idf(self, term: str) -> float:
        """How rare a term is. Rare term socres high, word in every chunk scores near zero."""
        n = len(self.chunks)
        df = self.doc_freq.get(term, 0)
        return math.log(1 + (n - df + 0.5) / (df + 0.5))


    def score(self, query_terms: list[str], position: int) -> float:
        """BM25 score of one chunk (by its position in the list)... for a list of query terms"""
        counts = self.term_counts[position]
        length_norm = 1- B + B * self.lengths[position] / self.avg_length
        total = 0.0
        for term in set(query_terms):
            tf = counts.get(term, 0)
            if tf:
                total += self.idf(term) * tf * (K1 + 1) / (tf + K1 * length_norm)
        return total


    def search(self, query: str, k: int = 10) -> list[dict]:
        """The k best chunks for a query... best first. Chunks that share no word with it are left out."""
        terms = tokenize(query)
        scored = []
        for position, chunk in enumerate(self.chunks):
            bm25 = self.score(terms, position)
            if bm25 > 0:
                scored.append({"chunk": chunk, "bm25": bm25})
        scored.sort(key=lambda hit: hit["bm25"], reverse=True)
        return scored[:k]









