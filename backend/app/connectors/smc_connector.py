"""
OZARK Backend — SMC Global Data Connector

Connects to SMC Global / SMC Institutional Research feeds.
Specializes in:
- Equity research coverage & fundamental investment ratings
- Corporate credit risk surveillance & loan against shares (LAS) tracking
- Derivative exposures & open interest concentration
- Corporate governance ranking and institutional sentiment
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


class SMCConnector(BaseConnector):
    """
    SMC Global Institutional Research & Credit Surveillance Connector.
    Provides mocked institutional metrics and risk advisory ratings.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.smcindiaonline.com/research/v1",
        timeout_seconds: int = 30,
        use_mock: bool = True,
    ):
        super().__init__(api_key=api_key, base_url=base_url, timeout_seconds=timeout_seconds, use_mock=use_mock)

    @property
    def source_name(self) -> str:
        return "SMC"

    async def fetch_company(self, identifier: str) -> ConnectorCompany:
        """Fetch SMC research universe entity profile and investment classification."""
        await asyncio.sleep(0.02)
        symbol = identifier.upper().strip()

        return ConnectorCompany(
            source=self.source_name,
            identifier=symbol,
            ticker=symbol,
            isin=f"INE{hash(symbol) % 90000000 + 10000000}014",
            name=f"{symbol} Global Holdings",
            legal_name=f"{symbol} Global Holdings Limited",
            status="ACTIVE",
            incorporation_date="2000-03-29",
            registered_state="Delhi",
            registered_address="11/6B, Shanti Chamber, Pusa Road, New Delhi - 110005",
            authorized_capital_inr=3500000000.0,
            paid_up_capital_inr=2900000000.0,
            industry="Capital Markets & Institutional Investment",
            sector="Financials",
            directors_count=8,
            raw_response={
                "smc_research_id": f"SMC_RES_{symbol}",
                "coverage_status": "ACTIVE_COVERAGE",
                "risk_category": "MODERATE_RISK",
            },
        )

    async def fetch_financials(self, identifier: str, years: int = 3) -> ConnectorFinancials:
        """Fetch SMC financial model projections, debt maturity schedule, and institutional estimates."""
        await asyncio.sleep(0.02)
        symbol = identifier.upper().strip()

        statements = []
        base_rev = 22000.0 + (abs(hash(symbol)) % 9000)
        base_profit = base_rev * 0.16

        for i in range(years):
            fy = f"FY{2024 - i}"
            factor = 1.0 - (i * 0.08)
            statements.append(
                FinancialYearRecord(
                    fiscal_year=fy,
                    revenue_inr_cr=round(base_rev * factor, 2),
                    operating_profit_inr_cr=round(base_profit * 1.28 * factor, 2),
                    net_profit_inr_cr=round(base_profit * factor, 2),
                    total_assets_inr_cr=round(base_rev * 1.9 * factor, 2),
                    total_debt_inr_cr=round(base_rev * 0.20 * factor, 2),
                    net_worth_inr_cr=round(base_rev * 1.45 * factor, 2),
                    operating_margin_pct=round(20.5 - (i * 0.4), 2),
                    debt_to_equity=round(0.14 + (i * 0.01), 2),
                    current_ratio=2.0,
                    interest_coverage_ratio=16.5,
                )
            )

        return ConnectorFinancials(
            source=self.source_name,
            identifier=symbol,
            currency="INR",
            unit="Crores (10M INR)",
            statements=statements,
            key_ratios={
                "institutional_sentiment_score": 8.4,
                "pledged_shares_risk_score": 1.2,
                "derivative_put_call_ratio": 0.88,
                "loan_against_shares_exposure_inr_cr": 45.0,
                "projected_cagr_3yr_pct": 14.5,
            },
            credit_rating="IND AAA",
            credit_outlook="POSITIVE",
            raw_response={
                "recommendation": "ACCUMULATE",
                "smc_target_inr": 2980.0,
                "governance_score": 88.0,
            },
        )

    async def fetch_compliance(self, identifier: str) -> ConnectorCompliance:
        """Fetch SMC credit risk review notes and forensic accounting alerts."""
        await asyncio.sleep(0.02)
        symbol = identifier.upper().strip()

        return ConnectorCompliance(
            source=self.source_name,
            identifier=symbol,
            compliance_score=91.5,
            status="COMPLIANT",
            filings=[
                ComplianceFiling(
                    filing_type="SMC_CREDIT_RISK_REPORT",
                    filing_date="2024-09-18",
                    status="APPROVED",
                    description="Forensic accounting audit: No circular transactions or promoter fund diversion detected.",
                )
            ],
            penalties=[],
            director_disqualifications_found=False,
            shell_company_signals_flagged=False,
            annual_general_meeting_date="2024-08-30",
            balance_sheet_filing_status="FILED",
            raw_response={
                "forensic_risk_flags": 0,
                "contingent_liabilities_to_networth_pct": 4.2,
            },
        )
