"""A labelled eval set for retrieval and answer quality.

Each answerable question records:
  doc_id    the document that holds the answer
  evidence  a short verbatim span from that document. A retrieved chunk counts as a hit
            only if it contains this exact span, so a chunk that cuts the span in half
            is a miss. That is deliberate: it is how chunking damage shows up in the numbers.
  keywords  what a correct answer must mention. Every item must appear in the answer.
            "a|b" means either a or b is acceptable. Matching is case-insensitive and
            whole-word, so "no" does not match inside "not". A trailing * allows any
            ending, so "exclud*" matches "excluded" and "excludes". A refusal never
            counts as correct, whatever words it happens to contain.
  kind      what the question tests

Unanswerable questions have doc_id None and no evidence. The correct behaviour is refusal.
"""

EVAL_SET = [
    # Harding & Voss (doc-101)
    {"id": "q01", "question": "By how much did Harding & Voss grow its revenue this year?",
     "doc_id": "doc-101", "evidence": "an increase of 4.1 percent", "keywords": ["4.1"], "kind": "numeric"},
    {"id": "q02", "question": "How many partners left Harding & Voss during the year?",
     "doc_id": "doc-101", "evidence": "Eleven partners left during the year", "keywords": ["eleven|11"], "kind": "title-dependent"},
    {"id": "q03", "question": "What share of Harding & Voss revenue comes from its disputes group?",
     "doc_id": "doc-101", "evidence": "41 percent of total revenue", "keywords": ["41"], "kind": "title-dependent"},
    {"id": "q04", "question": "When did Harding & Voss finish moving to a single document management platform?",
     "doc_id": "doc-101", "evidence": "single document management platform in May 2026", "keywords": ["May 2026"], "kind": "lookup"},
    {"id": "q05", "question": "Did Harding & Voss decide to open an office in New York?",
     "doc_id": "doc-101", "evidence": "reviewed a proposal for a New York office in February and rejected it", "keywords": ["reject*|no|not"], "kind": "negation"},

    # Marchetti Ruiz (doc-102)
    {"id": "q06", "question": "How big is the Marchetti Ruiz merit bonus pool?",
     "doc_id": "doc-102", "evidence": "12 percent of distributable profit", "keywords": ["12"], "kind": "lookup"},
    {"id": "q07", "question": "What do first-year associates at Marchetti Ruiz earn in New York?",
     "doc_id": "doc-102", "evidence": "a base salary of $225,000", "keywords": ["225"], "kind": "numeric"},
    {"id": "q08", "question": "How many lateral partners did Marchetti Ruiz hire this year?",
     "doc_id": "doc-102", "evidence": "hired 19 lateral partners", "keywords": ["19"], "kind": "numeric"},
    {"id": "q09", "question": "How concentrated is Marchetti Ruiz's client base?",
     "doc_id": "doc-102", "evidence": "account for 22 percent of revenue", "keywords": ["22"], "kind": "lookup"},
    {"id": "q10", "question": "How long does it take a Marchetti Ruiz partner to reach the top of the lockstep ladder?",
     "doc_id": "doc-102", "evidence": "takes nine years", "keywords": ["nine|9"], "kind": "lookup"},

    # Okonkwo Bell (doc-103)
    {"id": "q11", "question": "What combined capacity of offshore wind projects did Okonkwo Bell advise on?",
     "doc_id": "doc-103", "evidence": "combined capacity of 4.2 gigawatts", "keywords": ["4.2"], "kind": "numeric"},
    {"id": "q12", "question": "When will Okonkwo Bell consider a merger?",
     "doc_id": "doc-103", "evidence": "will not consider a merger before 2028", "keywords": ["2028"], "kind": "negation"},
    {"id": "q13", "question": "What share of Okonkwo Bell practice revenue comes from development finance institutions?",
     "doc_id": "doc-103", "evidence": "supplied 30 percent of practice revenue", "keywords": ["30"], "kind": "lookup"},
    {"id": "q14", "question": "Where did Okonkwo Bell open relationship offices?",
     "doc_id": "doc-103", "evidence": "relationship offices in Lagos and Nairobi", "keywords": ["Lagos", "Nairobi"], "kind": "lookup"},
    {"id": "q15", "question": "Which countries are Okonkwo Bell's green hydrogen mandates in?",
     "doc_id": "doc-103", "evidence": "in Namibia and Morocco", "keywords": ["Namibia", "Morocco"], "kind": "title-dependent"},

    # Sandoval Kerr (doc-104)
    {"id": "q16", "question": "Above what level of fees does Sandoval Kerr need risk partner sign-off?",
     "doc_id": "doc-104", "evidence": "above $2 million in expected fees", "keywords": ["2 million|2m|2,000,000"], "kind": "numeric"},
    {"id": "q17", "question": "How much professional indemnity cover does Sandoval Kerr carry in total?",
     "doc_id": "doc-104", "evidence": "excess layers to $400 million", "keywords": ["400 million|400m"], "kind": "numeric"},
    {"id": "q18", "question": "By how much did Sandoval Kerr's insurance premium rise?",
     "doc_id": "doc-104", "evidence": "The premium rose 18 percent", "keywords": ["18"], "kind": "numeric"},
    {"id": "q19", "question": "What is Sandoval Kerr's phishing simulation failure rate now?",
     "doc_id": "doc-104", "evidence": "from 9 percent to 3 percent", "keywords": ["3 percent|3%|three percent"], "kind": "title-dependent"},
    {"id": "q20", "question": "Does Sandoval Kerr have any outstanding regulatory matters?",
     "doc_id": "doc-104", "evidence": "has no outstanding regulatory matters", "keywords": ["no|none"], "kind": "negation"},

    # Lindqvist Partners (doc-105)
    {"id": "q21", "question": "How many lawyers work in Lindqvist Partners' Tokyo office?",
     "doc_id": "doc-105", "evidence": "It employs 38 lawyers", "keywords": ["38"], "kind": "heading-dependent"},
    {"id": "q22", "question": "When did Lindqvist Partners open its Sydney office?",
     "doc_id": "doc-105", "evidence": "opened in September 2025 with 14 lawyers", "keywords": ["September 2025"], "kind": "heading-dependent"},
    {"id": "q23", "question": "How many lawyers are in Lindqvist Partners' Singapore office?",
     "doc_id": "doc-105", "evidence": "now stands at 96 lawyers", "keywords": ["96"], "kind": "numeric"},
    {"id": "q24", "question": "What is matter LP-3307?",
     "doc_id": "doc-105", "evidence": "filed under matter reference LP-3307", "keywords": ["assessment"], "kind": "exact-id"},

    # Market, methodology, jurisdiction (doc-106 to doc-108)
    {"id": "q25", "question": "How many lateral partner moves were there in London this year?",
     "doc_id": "doc-106", "evidence": "to 412 moves", "keywords": ["412"], "kind": "numeric"},
    {"id": "q26", "question": "What share of London lateral partner hires went to US firms?",
     "doc_id": "doc-106", "evidence": "US firms accounted for 58 percent", "keywords": ["58"], "kind": "lookup"},
    {"id": "q27", "question": "How are fixed-share partners treated in the profit per equity partner benchmark?",
     "doc_id": "doc-107", "evidence": "Fixed-share partners are excluded from the equity partner count", "keywords": ["exclud*"], "kind": "rare-term"},
    {"id": "q28", "question": "Which exchange rate does the platform use to convert figures to US dollars?",
     "doc_id": "doc-107", "evidence": "average exchange rate for the financial year", "keywords": ["average"], "kind": "lookup"},
    {"id": "q29", "question": "How long must a lawyer practise under home title before seeking local admission?",
     "doc_id": "doc-108", "evidence": "After three years of regular practice", "keywords": ["three|3"], "kind": "lookup"},

    # Unanswerable: the corpus does not contain these answers
    {"id": "q30", "question": "What is the capital of France?",
     "doc_id": None, "evidence": None, "keywords": [], "kind": "unanswerable"},
    {"id": "q31", "question": "Who is the managing partner of Harding & Voss?",
     "doc_id": None, "evidence": None, "keywords": [], "kind": "unanswerable"},
    {"id": "q32", "question": "How many lawyers does Marchetti Ruiz employ in London?",
     "doc_id": None, "evidence": None, "keywords": [], "kind": "unanswerable"},
]


def answerable() -> list[dict]:
    return [q for q in EVAL_SET if q["doc_id"] is not None]


def unanswerable() -> list[dict]:
    return [q for q in EVAL_SET if q["doc_id"] is None]
