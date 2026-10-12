"""
OZARK Connectors — Moneycontrol Data Connector

Connects to Moneycontrol financial intelligence feeds.
Provides:
- fetch_company(identifier)
- fetch_financials(identifier, years)
- fetch_compliance(identifier)
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, Optional

from connectors.base import BaseConnector


class MoneycontrolConnector(BaseConnector):
    """Moneycontrol Financial & Market Intelligence Connector."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.moneycontrol.com/v1",
        timeout_seconds: int = 30,
        use_mock: bool = True,
        config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(api_key=api_key, base_url=base_url, timeout_seconds=timeout_seconds, use_mock=use_mock, config=config)

    @property
    def source_name(self) -> str:
        return "Moneycontrol"

    async def fetch_company(self, identifier: str) -> Dict[str, Any]:
        """Fetch Moneycontrol stock profile, sector categorization, and market identifiers."""
        await asyncio.sleep(0.02)
        symbol = identifier.upper().strip()

        return {
            "source": self.source_name,
            "identifier": symbol,
            "ticker": symbol,
            "isin": f"INE{hash(symbol) % 90000000 + 10000000}014",
            "name": f"{symbol} Enterprises Ltd",
            "legal_name": f"{symbol} Enterprises Public Limited",
            "status": "ACTIVE",
            "incorporation_date": "1998-11-12",
            "registered_state": "Karnataka",
            "registered_address": "Outer Ring Road, Bellandur, Bengaluru - 560103",
            "authorized_capital_inr": 5000000000.0,
            "paid_up_capital_inr": 3800000000.0,
            "industry": "IT Services & Consulting",
            "sector": "Information Technology",
            "directors_count": 10,
            "raw_response": {
                "mc_scrip_code": f"MC_{symbol}",
                "bse_code": f"5{hash(symbol) % 90000 + 10000}",
                "nse_symbol": symbol,
                "market_cap_tier": "Large Cap",
            },
            "fetched_at": datetime.utcnow().isoformat(),
        }

    async def fetch_financials(self, identifier: str, years: int = 3) -> Dict[str, Any]:
        """Fetch Moneycontrol consolidated financial statements and fundamental valuation metrics."""
        await asyncio.sleep(0.02)
        symbol = identifier.upper().strip()

        statements = []
        base_rev = 28000.0 + (abs(hash(symbol)) % 15000)
        base_profit = base_rev * 0.19

        for i in range(years):
            fy = f"FY{2024 - i}"
            factor = 1.0 - (i * 0.09)
            statements.append({
                "fiscal_year": fy,
                "revenue_inr_cr": round(base_rev * factor, 2),
                "operating_profit_inr_cr": round(base_profit * 1.35 * factor, 2),
                "net_profit_inr_cr": round(base_profit * factor, 2),
                "total_assets_inr_cr": round(base_rev * 2.1 * factor, 2),
                "total_debt_inr_cr": round(base_rev * 0.12 * factor, 2),
                "net_worth_inr_cr": round(base_rev * 1.65 * factor, 2),
                "operating_margin_pct": round(24.2 - (i * 0.4), 2),
                "debt_to_equity": round(0.08 + (i * 0.01), 2),
                "current_ratio": 2.4,
                "interest_coverage_ratio": 28.5,
            })

        return {
            "source": self.source_name,
            "identifier": symbol,
            "currency": "INR",
            "unit": "Crores (10M INR)",
            "statements": statements,
            "key_ratios": {
                "price_to_earnings_ttm": 31.8,
                "price_to_book": 7.4,
                "ev_to_ebitda": 21.2,
                "return_on_equity_pct": 26.8,
                "return_on_capital_employed_pct": 32.4,
                "dividend_yield_pct": 1.45,
            },
            "credit_rating": "ICRA AAA",
            "credit_outlook": "STABLE",
            "raw_response": {"broker_consensus": "BUY", "target_price_inr": 3850.0, "analysts_covering": 38},
            "fetched_at": datetime.utcnow().isoformat(),
        }

    async def fetch_compliance(self, identifier: str) -> Dict[str, Any]:
        """Fetch Moneycontrol governance check and corporate actions log."""
        await asyncio.sleep(0.02)
        symbol = identifier.upper().strip()

        return {
            "source": self.source_name,
            "identifier": symbol,
            "compliance_score": 92.0,
            "status": "COMPLIANT",
            "filings": [
                {
                    "filing_type": "BOARD_MEETING_OUTCOME",
                    "filing_date": "2024-10-01",
                    "status": "APPROVED",
                    "description": "Board approved Q2 financial results and interim dividend of INR 12 per share.",
                }
            ],
            "penalties": [],
            "director_disqualifications_found": False,
            "shell_company_signals_flagged": False,
            "annual_general_meeting_date": "2024-07-18",
            "balance_sheet_filing_status": "FILED",
            "raw_response": {"audit_quality_score": 9.2, "governance_rating": "EXCELLENT"},
            "fetched_at": datetime.utcnow().isoformat(),
        }
