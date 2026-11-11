"""The Week 4 corpus: eight long, sectioned documents.

Synthetic, written for teaching. Figures agree with data.py where they overlap.
Sections start with '## ' so a chunker can find them. Some sections never repeat the
firm or office name in their body text on purpose: the heading carries that meaning.
"""

CORPUS_DOCUMENTS = [
    {
        "id": "doc-101",
        "title": "Harding & Voss: Annual Strategy Review",
        "firm_id": 1,
        "type": "strategy",
        "body": """## Overview
Harding & Voss closed its financial year with revenue of $1.24 billion, an increase of 4.1 percent on the prior year. The firm employs 1,850 lawyers across nine offices, and the equity partnership stands at 210. Management describes the year as one of consolidation rather than expansion. Growth came almost entirely from existing clients, and the firm made no acquisitions. The managing partner told the partnership that the priority for the next two years is margin, not size.

## Disputes
The disputes group remains the strongest part of the business. It generated 41 percent of total revenue, up from 37 percent two years ago. Commercial litigation and international arbitration account for most of that work. The group won a long-running shipping arbitration seated in Singapore in the third quarter, which brought in a significant success fee. Four of the five lateral partners hired in the last three years joined this group. Clients cite responsiveness and the seniority of the team that actually does the work.

## Corporate
The corporate team is competent but has not won a significant mandate outside the UK in the last eighteen months. It advised on 23 mid-market transactions during the year, with an average deal value of roughly £85 million. Private equity work is thin, and the team has lost two pitches to US firms with larger London offices. A review of the corporate strategy is due to report to the board before the summer.

## People and retention
Partner retention is good. Eleven partners left during the year, against a ten-year average of fourteen. Associate attrition fell to 16 percent, the lowest figure the firm has recorded. The firm introduced a formal sabbatical scheme for senior associates and expanded its parental leave policy. Exit interviews point to workload in the corporate team as the most common reason for leaving.

## Technology
The firm completed its move to a single document management platform in May 2026. Spending on technology rose to 3.2 percent of revenue. A contract review tool, built with a third-party vendor, is in pilot with the real estate team. Early results suggest first-pass review time has fallen, although lawyers still check every flagged clause by hand. The firm has not yet set a budget for wider adoption.

## United States
Harding & Voss does not operate in the United States and has no plans to open there. The board reviewed a proposal for a New York office in February and rejected it. Instead the firm relies on referral relationships with two US firms, which send it English law work and receive its US matters in return. Partners describe the arrangement as cheap and flexible, but it caps the firm's ability to compete for the largest transatlantic mandates.

## Clients
The client base is stable and heavily weighted towards financial institutions and insurers. The top twenty clients generated just over a third of revenue, a share that has barely moved in five years. The firm won panel appointments with two clearing banks during the year and lost one insurance panel after a procurement exercise that it described as decided on price. Relationship partners now meet each top-twenty client at least twice a year, and a client listening programme run by an external agency interviewed forty general counsel. The most common criticism was the cost of junior time on large disputes, and the firm has since capped junior hours on several fixed-fee matters.

## Pricing
Around a quarter of fees are now agreed on a fixed or capped basis, up from a fifth three years ago. The pricing team reviews every bid above a set value and tracks write-offs by practice. Write-offs fell slightly during the year, but remain highest in the corporate team, where competitive pressure on mid-market deals is strongest. The firm has resisted discounting its disputes rates and believes the practice can sustain its current pricing for at least another year.

## Outlook
Management expects revenue growth of between 3 and 5 percent next year. The main risks are a slowdown in arbitration filings and continued pressure on corporate pricing. The firm does not plan to open new offices.
""",
    },
    {
        "id": "doc-102",
        "title": "Marchetti Ruiz: Partner Compensation and Growth Report",
        "firm_id": 2,
        "type": "compensation",
        "body": """## Summary
Marchetti Ruiz reported revenue of $2.98 billion for the year, with 2,400 lawyers and 340 equity partners. It remains the largest firm in this peer group by both revenue and headcount. Profit growth outpaced revenue growth for the third year running, helped by tight control of support costs.

## Compensation model
The firm runs a modified lockstep. Partners progress up a ladder of points, and progression from entry to the top of the ladder takes nine years. On top of the lockstep, a merit bonus pool equal to 12 percent of distributable profit is shared each year by a compensation committee. Partners can be moved down the ladder for sustained underperformance, although this has happened only twice in five years. The committee publishes its criteria internally but not the individual awards.

## The US practice
The US practice drives the majority of profitability. It contributes 68 percent of firm profit while accounting for a little over half of headcount. New York and Washington are the two largest offices. Regulatory work in Washington has grown faster than any other practice over the last two years.

## Associate pay
First-year associates in New York earn a base salary of $225,000. The firm matches the market scale set by its New York competitors and pays year-end bonuses on the same scale. Associate pay in London follows a separate scale that sits slightly below the US firms with the largest London offices.

## Lateral activity
The firm hired 19 lateral partners during the year, mostly in private equity and funds. It lost seven partners over the same period, four of them to a single competitor. Lateral hires are guaranteed their points for two years, after which they join the normal review cycle.

## Office network
New York and Washington are the two largest offices by headcount, followed by Chicago, London and Houston. The London office has grown steadily and now handles most of the firm's European private equity work, although it remains small relative to the US offices. The firm closed a small office in Frankfurt during the year after failing to recruit enough local partners to make it viable. Office leases in New York and Washington run until 2034, which the finance committee regards as a fixed cost that limits flexibility in a downturn.

## Diversity
Women make up 31 percent of the equity partnership, up from 26 percent five years ago. The firm has a published target of 35 percent by the end of the decade. Progress has been fastest among partners promoted internally; lateral hiring has done less to improve the figures, because most lateral partners come from practice areas that are themselves male-dominated. The compensation committee now reviews points allocations for unexplained gaps before they are confirmed.

## Risks
Client concentration is the main risk flagged by the finance committee. The top ten clients account for 22 percent of revenue, and the largest single client accounts for just under 4 percent. The committee has asked practice leaders to report quarterly on new client wins.
""",
    },
    {
        "id": "doc-103",
        "title": "Okonkwo Bell: Energy Transition Practice Profile",
        "firm_id": 3,
        "type": "practice",
        "body": """## Overview
Okonkwo Bell has a deliberately narrow focus. The firm has 910 lawyers and has built its reputation in energy and infrastructure work, particularly projects with a development finance element. It is not trying to be a full-service firm and has turned away work outside its core areas. Headcount has grown slowly and deliberately.

## Offshore wind
Offshore wind is the largest single area of work. During the year the firm advised on six offshore wind projects with a combined capacity of 4.2 gigawatts, four of them in the North Sea. Most mandates came from sponsors rather than lenders. Fee pressure in this market is rising as more firms compete for the same projects.

## Development finance
Work for multilateral lenders and export credit agencies sets the firm apart. Development finance institutions supplied 30 percent of practice revenue during the year. These relationships are long-standing and rarely go to competitive tender, which gives the firm unusually predictable income.

## Clients and sponsors
The client list is concentrated among a few dozen sponsors, utilities and lenders who return year after year. Repeat instructions account for most new matters, and the firm rarely pitches for one-off work. Sponsors value the firm's experience of taking projects from early development through to financial close, often over five years or more. Several of the largest clients have used the firm on every project they have developed in Africa.

## Merger approaches
The firm's leadership has been explicit that it does not intend to merge, and it has declined at least two approaches in the past three years. The senior partner told staff that the firm will not consider a merger before 2028 at the earliest. Partners see independence as part of the firm's appeal to development finance clients, who value a firm without conflicts from a large corporate client base.

## Africa desk
The firm opened relationship offices in Lagos and Nairobi in 2024. These are not full offices: they are staffed by business development teams and a small number of seconded lawyers, and all legal work is billed from London. Instructions from African sponsors have grown steadily since they opened.

## Recruitment
Hiring is slow and deliberate. The firm recruits most of its associates from a small number of universities with strong energy law programmes, and it trains them in-house rather than hiring laterally at mid-level. Associate retention is high by industry standards, which partners attribute to the firm's narrow focus and the chance to work on projects that run for several years. The firm has not hired a lateral partner since 2021.

## Hydrogen
Green hydrogen remains early-stage. The firm holds three green hydrogen mandates, in Namibia and Morocco, all at the feasibility stage. Partners expect the practice to remain small until projects reach financial close.
""",
    },
    {
        "id": "doc-104",
        "title": "Sandoval Kerr: Risk, Compliance and Insurance Review",
        "firm_id": 4,
        "type": "risk",
        "body": """## Background
Sandoval Kerr has invested heavily in its conflicts and compliance function following a difficult period two years ago, when the firm acted for two clients on opposite sides of the same transaction without spotting the conflict. The matter settled confidentially. The review that followed rebuilt the intake process from the ground up.

## Intake controls
The matter intake process now requires sign-off from a dedicated risk partner for any engagement above $2 million in expected fees. Smaller engagements are cleared by the conflicts team alone. Average clearance time rose from two days to three after the change, which partners initially resisted but now accept. Every lateral hire's client list is screened before an offer is made.

## Insurance
Professional indemnity arrangements were renegotiated at the last renewal. The firm carries a primary layer of $50 million, with excess layers to $400 million. The premium rose 18 percent, which the broker attributed partly to the conflicts matter and partly to wider market conditions.

## Regulatory position
The firm has no outstanding regulatory matters and has notified its insurers of no material claims this year. The general counsel reports directly to the management committee rather than to the managing partner.

## Client terms
Engagement letters were rewritten after the review. They now state the scope of each engagement more tightly, limit liability where the client agrees, and require clients to disclose related parties at the outset. Partners must record a reason whenever they depart from the standard terms. The general counsel's team audits a sample of engagement letters every quarter and reports exceptions to the management committee.

## Training
Every fee earner completes four hours of conflicts and ethics training each year, and completion is a condition of the annual pay review. Partners complete an additional session on engagement terms.

## Cyber security
The firm runs monthly phishing simulations. The simulation failure rate fell from 9 percent to 3 percent over the year, the lowest figure since the programme began. Two-factor authentication is now mandatory on every device that can reach client data.
""",
    },
    {
        "id": "doc-105",
        "title": "Lindqvist Partners: APAC Expansion Review",
        "firm_id": 5,
        "type": "expansion",
        "body": """## Overview
Lindqvist Partners is a Nordic-heritage firm with 520 lawyers. Its APAC strategy leans on relationships with Nordic corporates operating in the region rather than on local market share. This has produced a profitable but narrow practice. The board commissioned this review to decide which APAC offices to grow, hold or close.

## Singapore
Singapore is the fastest-growing part of the business. Headcount has doubled since 2022 and now stands at 96 lawyers. Most of the work is energy, shipping and infrastructure for Nordic clients, and the office is profitable on every measure the firm uses.

## Tokyo
The office has underperformed against its original business case and is under review. It employs 38 lawyers, against the 60 forecast when it opened. Revenue per lawyer is the lowest in the firm. The board's assessment of the office is filed under matter reference LP-3307 and is not for external circulation. A decision is expected by the end of the first quarter.

## Hong Kong
The firm closed this office in 2023 and transferred its work and remaining lawyers to Singapore. No partners left the firm as a result of the closure.

## Sydney
The office opened in September 2025 with 14 lawyers, most of them transferred from Singapore. It serves Nordic mining and renewables clients and has not yet reached break-even. The business case assumes it will do so in its third year.

## Shanghai representative office
The firm keeps a two-person representative office in Shanghai, which supports Nordic manufacturers with operations in China. It does not practise Chinese law and refers that work to local firms. The office costs little to run and the review recommends keeping it open, although it notes that client demand has fallen as several Nordic manufacturers have moved production elsewhere in Asia.

## Talent and secondments
Most APAC partners began their careers in the Nordic offices and transferred out on secondment. The firm offers associates two-year secondments to Singapore, which are heavily oversubscribed. The review warns that relying on transfers from the Nordic offices makes it hard to build local client relationships, and recommends hiring at least two partners locally in Singapore over the next three years.

## Outlook
The review recommends continued investment in Singapore and Sydney. The recommendation on Tokyo is deferred until the internal assessment is complete.
""",
    },
    {
        "id": "doc-106",
        "title": "UK Lateral Hiring Market Report",
        "firm_id": None,
        "type": "market",
        "body": """## Headline numbers
Lateral partner moves in the London market rose 9 percent this year, to 412 moves. The increase was concentrated in the second half of the year, after a slow first quarter. Moves between UK firms were broadly flat; the growth came from firms headquartered elsewhere.

## Practice areas
Private equity was the most active practice area, accounting for 21 percent of moves, followed by disputes and then finance. Real estate and employment saw the fewest moves. Recruiters expect private equity to remain the busiest area while deal activity recovers.

## US firms in London
US firms accounted for 58 percent of lateral partner hires, their highest share on record. Their offers typically combine higher pay with multi-year guarantees, which UK firms find hard to match without disrupting their own compensation systems.

## Guarantees
Multi-year guarantees now feature in roughly one in three moves. Most run for two years, and a minority run for three. Recruiters report that candidates increasingly ask for guarantees before discussing anything else.

## Regional markets
Manchester and Birmingham both saw more lateral activity than last year, mostly from firms opening or expanding regional offices to reduce costs. Partner pay in the regions remains well below London.

## Associate market
Associate moves were busier than partner moves. Demand was strongest for mid-level associates with three to five years' experience in finance and private equity, and several firms offered retention bonuses to stop their own associates leaving. Salaries for newly qualified solicitors in London reached new highs at the US firms, widening the gap with the largest UK firms. Recruiters report that candidates at this level increasingly ask about hybrid working before they ask about pay.

## In-house moves
A growing number of senior associates and junior partners moved in-house during the year, particularly to banks, private equity houses and technology companies. Recruiters attribute this partly to working hours and partly to the improved pay on offer in-house. Several firms now run alumni programmes to keep in touch with former lawyers, who are often a source of future instructions.

## Outlook
Recruiters expect activity to remain high next year, but warn that a slowdown in deal activity would hit private equity moves first.
""",
    },
    {
        "id": "doc-107",
        "title": "Benchmarking Methodology Handbook",
        "firm_id": None,
        "type": "methodology",
        "body": """## Purpose
This handbook explains how the platform calculates the benchmarks it reports for each firm. Users should read it before comparing firms, because small differences in definition can produce large differences in the numbers.

## Revenue per lawyer
Revenue per lawyer is total revenue divided by fee-earner headcount. Fee earners include partners, associates and other qualified lawyers who record billable time. Trainees and support staff are excluded. The figure is a rough measure of productivity and is sensitive to the mix of practices a firm runs.

## Profit per equity partner
The platform assumes a 35 percent profit margin, multiplies revenue by that margin, and divides the result by the number of equity partners. Where a firm publishes its actual profit, the published figure replaces the assumed margin. The assumed margin overstates profit per equity partner for firms with high fixed costs, such as those with large real estate commitments.

## Fixed-share partners
Fixed-share partners are excluded from the equity partner count. They are treated as fee earners for revenue per lawyer, so a firm that moves partners from equity to fixed share will see its profit per equity partner rise without any change in underlying profitability. Analysts should check for changes in partnership structure before reading too much into a rise.

## Currency
All figures are converted to US dollars at the average exchange rate for the financial year, not the rate at the year end. This avoids distortions from currency movements late in the year.

## Peer groups
The platform compares each firm against a peer group of firms of similar size and practice mix. Peer groups are reviewed once a year. A firm that changes its practice mix sharply, for example by selling a business line, may move into a different peer group, and comparisons with its previous peers should be treated with care.

## Data sources
Figures come from published accounts where a firm publishes them, and from firm submissions and market estimates where it does not. Every figure in the platform carries a source flag. Estimated figures are marked as such and should not be compared directly with audited figures from another firm.

## Headcount
Headcount figures use the average of opening and closing headcount for the year, so a firm that hires heavily in the final month does not see its revenue per lawyer fall sharply.
""",
    },
    {
        "id": "doc-108",
        "title": "EU Practice Rights: Jurisdiction Note",
        "firm_id": None,
        "type": "jurisdiction",
        "body": """## Practising under home title
Lawyers qualified in one EU member state may practise in another under their home title, under the Establishment Directive. They must register with the competent authority in the host state. After three years of regular practice in the host state's law, they may seek admission to the local profession without sitting the usual aptitude test.

## UK lawyers after Brexit
UK-qualified lawyers lost the automatic right to practise under home title in the EU when the transition period ended. Their position now depends on the rules of each member state. Some allow UK lawyers to give advice on English and international law; others restrict them more tightly.

## Ireland
Many UK solicitors registered in Ireland before the end of the transition period so that they could continue to practise EU law. To keep that status, a solicitor must hold an Irish practising certificate and, in most cases, practise from an Irish office.

## Multidisciplinary practices
Several member states restrict partnerships between lawyers and other professionals. France and Germany both limit external ownership of law firms, which affects firms that want to offer combined legal and consulting services.

## Switzerland and the EEA
The Establishment Directive applies across the European Economic Area, so lawyers from Norway, Iceland and Liechtenstein have broadly the same rights as lawyers from EU member states. Switzerland is not part of the EEA but has a separate agreement with the EU that gives EU lawyers similar rights to provide services there. Neither arrangement now benefits UK lawyers.

## Temporary services
Lawyers from an EU member state may also provide services in another member state on a temporary basis without registering, under the Lawyers' Services Directive. They must use their home title and, in litigation, may be required to work with a local lawyer. Temporary services suit occasional work but not a permanent practice.

## Implications for firms in this platform
Firms without EU-qualified partners in the relevant member state should assume that they need local counsel for any work governed by that state's law.
""",
    },
]
