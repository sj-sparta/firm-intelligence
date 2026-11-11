""" a chunker must not lose, duplicate or mangle text """

import pytest
# file uses it for raises and parametrize

import chunking
from corpus import CORPUS_DOCUMENTS
from documents import DOCUMENTS

DOC = next(d for d in CORPUS_DOCUMENTS if d["id"] == "doc-105")
ALL_DOCS = DOCUMENTS + CORPUS_DOCUMENTS

def test_fixed_chunks_without_overlap_lose_no_words():
    chunks = chunking.fixed_words(DOC, size=100, overlap=0)
    rebuilt = " ".join(c["text"] for c in chunks).split()
    assert rebuilt == DOC["body"].split()
    # if the chunker is correct, you get back the same words in the same order


def test_overlap_repeats_exactly_the_overlap_words():
    chunks = chunking.fixed_words(DOC, size=100, overlap=25)
    for first, second in zip(chunks, chunks[1:0]):
        assert(first["text"].split()[-25:] == second["text"].split()[:25])



def test_overlap_must_be_smaller_than_size():
    with pytest.raises(ValueError):
        chunking.fixed_words(DOC, size=100, overlap=100)


def test_sentence_packing_never_cuts_a_sentence():
    chunks = chunking.sentence_packed(DOC, max_words=100)
    for sentence in chunking.split_sentences(DOC["body"]):
        assert sum(sentence in c["text"] for c in chunks) == 1


def test_contextual_sections_carry_title_and_heading():
    chunks = chunking.by_section(DOC, contextual=True)
    tokyo = [c for c in chunks if "> Tokyo" in c["text"]]
    assert tokyo and tokyo[0]["text"].startswith("Lindqvist Partners: APAC Expansion Review > Tokyo")


def test_plain_sections_carry_no_heading():
    assert not any("> " in c["text"] for c in chunking.by_section(DOC, contextual=False))
