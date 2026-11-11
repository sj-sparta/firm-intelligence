from typing import Any

FIRMS: list[dict[str, Any]] = [
    {"id": 1, "name": "Harding & Voss", "jurisdiction": "UK",
     "revenue_usd_m": 1240, "lawyers": 1850, "equity_partners": 210},
    {"id": 2, "name": "Marchetti Ruiz", "jurisdiction": "US",
     "revenue_usd_m": 2980, "lawyers": 2400, "equity_partners": 340},
    {"id": 3, "name": "Okonkwo Bell", "jurisdiction": "UK",
     "revenue_usd_m": 640, "lawyers": 910, "equity_partners": 115},
    {"id": 4, "name": "Sandoval Kerr", "jurisdiction": "US",
     "revenue_usd_m": 1875, "lawyers": 1620, "equity_partners": 265},
    {"id": 5, "name": "Lindqvist Partners", "jurisdiction": "APAC",
     "revenue_usd_m": 410, "lawyers": 520, "equity_partners": 68},
]




PEOPLE: list[dict[str, Any]] = [
    {"id": 1, "name": "Priya Chandrasekaran", "role": "Equity Partner", "firm_id": 1},
    {"id": 2, "name": "Tom Whitfield", "role": "Associate", "firm_id": 1},
    {"id": 3, "name": "Elena Marchetti", "role": "Equity Partner", "firm_id": 2},
    {"id": 4, "name": "Kwame Boateng", "role": "Associate", "firm_id": 3},
]