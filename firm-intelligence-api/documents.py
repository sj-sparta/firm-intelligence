"""The document corpus. SYNTHETIC PLACEHOLDER CONTENT ONLY.

Unlike data.py, which holds structured records, this holds prose - the kind of
unstructured text a client would actually have sitting in SharePoint.
"""

from typing import Any

DOCUMENTS: list[dict[str, Any]] = [
    {
        "id": "doc-001",
        "title": "Harding & Voss — Market Position Note",
        "firm_id": 1,
        "type": "market-note",
        "body": (
            "Harding & Voss remains one of the stronger mid-tier performers in the UK "
            "market. Revenue growth has been steady rather than spectacular, and the "
            "firm has resisted the temptation to chase headline lateral hires. Its "
            "disputes practice is widely regarded as the strongest part of the "
            "business, particularly in commercial litigation and international "
            "arbitration. The corporate team is competent but has not won a "
            "significant mandate outside the UK in the last eighteen months. "
            "Partner retention is good. The firm does not operate in the United States "
            "and has no plans to open there."
        ),
    },
    {
        "id": "doc-002",
        "title": "Marchetti Ruiz — Compensation Review",
        "firm_id": 2,
        "type": "compensation",
        "body": (
            "Marchetti Ruiz operates a modified lockstep model with a significant "
            "discretionary element at the top of the equity. This has allowed the firm "
            "to compete for high performers without abandoning its collegiate culture "
            "entirely. Profit per equity partner has grown consistently, though the "
            "gap between the top and bottom of equity has widened to a ratio that some "
            "partners consider unsustainable. The firm's US practice drives the "
            "majority of profitability. Associate compensation was reviewed in the "
            "last cycle and brought broadly in line with the market."
        ),
    },
    {
        "id": "doc-003",
        "title": "Okonkwo Bell — Strategy Briefing",
        "firm_id": 3,
        "type": "strategy",
        "body": (
            "Okonkwo Bell is a boutique with a deliberately narrow focus. The firm has "
            "built a reputation in energy and infrastructure work, particularly "
            "projects with a development finance element. It is not trying to be a "
            "full-service firm and has turned away work outside its core areas. "
            "Headcount has grown slowly and deliberately. The firm's leadership has "
            "been explicit that it does not intend to merge, and has declined at least "
            "two approaches in the past three years."
        ),
    },
    {
        "id": "doc-004",
        "title": "Sandoval Kerr — Risk and Compliance Summary",
        "firm_id": 4,
        "type": "compliance",
        "body": (
            "Sandoval Kerr has invested heavily in its conflicts and compliance "
            "function following a difficult period two years ago. The firm's matter "
            "intake process now requires sign-off from a dedicated risk partner for "
            "any engagement above a defined threshold. Professional indemnity "
            "arrangements were renegotiated at the last renewal. There are no "
            "outstanding regulatory matters. The firm reports no material claims "
            "in the current period."
        ),
    },
    {
        "id": "doc-005",
        "title": "Lindqvist Partners — APAC Expansion Review",
        "firm_id": 5,
        "type": "strategy",
        "body": (
            "Lindqvist Partners has grown its Singapore office faster than any other "
            "part of the business. The firm's APAC strategy leans on relationships "
            "with Nordic corporates operating in the region rather than on local "
            "market share. This has produced a profitable but narrow practice. The "
            "Tokyo office has underperformed against its original business case and "
            "is under review. Matter reference LP-2291 covers the internal assessment "
            "of that review and is not for external circulation."
        ),
    },
    {
        "id": "doc-006",
        "title": "UK Market Commentary — Lateral Hiring",
        "firm_id": None,
        "type": "market-note",
        "body": (
            "Lateral partner hiring across the UK market slowed in the most recent "
            "period, reversing three years of aggressive recruitment. Firms that "
            "over-extended on guaranteed packages are now carrying underperforming "
            "partners they cannot easily exit. The firms that held their discipline "
            "are in a materially better position. Disputes practices continue to "
            "attract the most competitive offers, while transactional teams have seen "
            "offers flatten."
        ),
    },
    {
        "id": "doc-007",
        "title": "Jurisdiction Note — EU Practice Rights",
        "firm_id": None,
        "type": "regulatory",
        "body": (
            "Firms operating across EU member states continue to navigate divergent "
            "requirements on practice rights and establishment. The position for "
            "UK-qualified lawyers has not returned to the pre-2021 arrangement. Firms "
            "with a registered EU presence are largely unaffected. Those servicing EU "
            "clients from London face more friction, particularly in regulated "
            "advisory work. Reference EUPR-14 sets out the current position per "
            "jurisdiction."
        ),
    },
    {
        "id": "doc-008",
        "title": "Benchmarking Methodology",
        "firm_id": None,
        "type": "methodology",
        "body": (
            "Revenue per lawyer is calculated as total revenue divided by total "
            "fee-earner headcount, excluding business services staff. Profit per "
            "equity partner assumes a thirty-five per cent margin applied to revenue, "
            "then divided by the number of full equity partners. Fixed-share partners "
            "are excluded from that denominator. These figures are indicative and "
            "should not be compared across jurisdictions without adjustment for "
            "local cost bases."
        ),
    },
]
