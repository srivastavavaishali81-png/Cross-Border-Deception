"""
OZARK Backend — SEBI Data Connector

Connects to Securities and Exchange Board of India (SEBI) regulatory registry.
Monitors:
- Listed disclosures & SCORES investor grievances
- Prohibition & Adjudication orders (PIT Regulations / Insider Trading)
- Takeover Code (SAST) filings & Substantial Acquisitions
- LODR Compliance filings
"""

import asyncio
from datetime import datetime
from typing import Optional

from app.connectors.base import (
    BaseConnector,
    ComplianceFiling,
    ConnectorCompany,
    ConnectorCompliance,
    ConnectorFinancials,
    FinancialYearRecord,
    RegulatoryPenalty,
)


class SEBIConnector(BaseConnector):
    """
    SEBI (Securities and Exchange Board of India) Regulatory Connector.
    Provides mocked compliance and enforcement intelligence prepared for live API integration.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.sebi.gov.in/v2",
        timeout_seconds: int = 30,
        use_mock: bool = True,
    ):
        super().__init__(api_key=api_key, base_url=base_url, timeout_seconds=timeout_seconds, use_mock=use_mock)

    @property
    def source_name(self) -> str:
        return "SEBI"

    async def fetch_company(self, identifier: str) -> ConnectorCompany:
        """Fetch SEBI entity registration, scrip listing status, and ISIN master data."""
        await asyncio.sleep(0.02)  # Simulate non-blocking I/O
        symbol = identifier.upper().strip()

        return ConnectorCompany(
            source=self.source_name,
            identifier=symbol,
            isin=f"INE{hash(symbol) % 90000000 + 10000000}014",
            ticker=symbol,
            name=f"{symbol} Corporation Limited",
            legal_name=f"{symbol} Corporation Limited (Listed on NSE/BSE)",
            status="ACTIVE",
            incorporation_date="2002-04-18",
            registered_state="Maharashtra",
            registered_address="SEBI Registered Exchange Tower, BKC, Mumbai - 400051",
            authorized_capital_inr=1500000000.0,
            paid_up_capital_inr=1200000000.0,
            industry="Technology & Industrial Manufacturing",
            sector="Large Cap Equity",
            directors_count=8,
            raw_response={
                "sebi_registration_number": f"IN-EQ-{symbol}-2024",
                "listing_exchanges": ["NSE", "BSE"],
                "market_lot": 1,
                "scores_registration": True,
            },
        )

    async def fetch_financials(self, identifier: str, years: int = 3) -> ConnectorFinancials:
        """Fetch SEBI Regulation 33 quarterly and annual audited financial disclosures."""
        await asyncio.sleep(0.02)
        symbol = identifier.upper().strip()

        # Generate realistic financial statement records
        statements = []
        base_rev = 14500.0 + (abs(hash(symbol)) % 10000)
        base_profit = base_rev * 0.16

        for i in range(years):
            fy = f"FY{2024 - i}"
            factor = 1.0 - (i * 0.08)
            statements.append(
                FinancialYearRecord(
                    fiscal_year=fy,
                    revenue_inr_cr=round(base_rev * factor, 2),
                    operating_profit_inr_cr=round(base_profit * factor * 1.2, 2),
                    net_profit_inr_cr=round(base_profit * factor, 2),
                    total_assets_inr_cr=round(base_rev * 1.8 * factor, 2),
                    total_debt_inr_cr=round(base_rev * 0.25 * factor, 2),
                    net_worth_inr_cr=round(base_rev * 1.2 * factor, 2),
                    operating_margin_pct=round(18.5 - (i * 0.5), 2),
                    debt_to_equity=round(0.22 + (i * 0.02), 2),
                    current_ratio=1.85,
                    interest_coverage_ratio=9.4,
                )
            )

        return ConnectorFinancials(
            source=self.source_name,
            identifier=symbol,
            currency="INR",
            unit="Crores (10M INR)",
            statements=statements,
            key_ratios={
                "price_to_earnings": 28.4,
                "promoter_pledge_percentage": 0.0,
                "public_shareholding_percentage": 48.2,
                "institutional_holding_percentage": 34.6,
            },
            credit_rating="CRISIL AAA",
            credit_outlook="STABLE",
            raw_response={"filing_regulation": "SEBI LODR Reg 33", "auditor_opinion": "UNQUALIFIED"},
        )

    async def fetch_compliance(self, identifier: str) -> ConnectorCompliance:
        """Fetch SEBI enforcement orders, PIT compliance, and LODR disclosures."""
        await asyncio.sleep(0.02)
        symbol = identifier.upper().strip()
        is_flagged = "FRAUD" in symbol or "WARN" in symbol

        filings = [
            ComplianceFiling(
                filing_type="SEBI_LODR_REG_30",
                filing_date="2024-09-15",
                status="APPROVED",
                form_id="SEBI-REG30-98421",
                description="Material event disclosure: Expansion of automated manufacturing facility.",
            ),
            ComplianceFiling(
                filing_type="SEBI_SAST_REG_29",
                filing_date="2024-06-30",
                status="APPROVED",
                form_id="SEBI-SAST-54219",
                description="Disclosure of promoter group shareholding reconciliation.",
            ),
            ComplianceFiling(
                filing_type="SEBI_PIT_BENPOS",
                filing_date="2024-03-31",
                status="APPROVED",
                form_id="SEBI-PIT-11984",
                description="Quarterly Benpos insider trading structured digital database (SDD) audit.",
            ),
        ]

        penalties = []
        if is_flagged:
            penalties.append(
                RegulatoryPenalty(
                    authority="SEBI Adjudication Division",
                    order_date="2024-05-12",
                    section_violated="Section 15A(b) of SEBI Act, 1992 - Delayed LODR Disclosures",
                    penalty_amount_inr=1500000.0,
                    adjudication_status="SETTLED",
                    summary="Penalty imposed for 14-day delay in disclosure of key board changes.",
                )
            )

        return ConnectorCompliance(
            source=self.source_name,
            identifier=symbol,
            compliance_score=68.0 if is_flagged else 94.5,
            status="DEFICIENT" if is_flagged else "COMPLIANT",
            filings=filings,
            penalties=penalties,
            director_disqualifications_found=False,
            shell_company_signals_flagged=is_flagged,
            annual_general_meeting_date="2024-08-22",
            balance_sheet_filing_status="FILED",
            raw_response={
                "scores_pending_complaints": 1 if is_flagged else 0,
                "sdd_compliance_certified": not is_flagged,
            },
        )
