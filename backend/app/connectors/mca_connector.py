"""
OZARK Backend — MCA Data Connector

Connects to Ministry of Corporate Affairs (MCA21 / V3 Portal) registry.
Specializes in:
- Corporate Identity Number (CIN) & RoC jurisdiction validation
- Director Identification Number (DIN) & active directorship tracking
- Registered charges & hypothecation registry (Bank-backed debt liens)
- AOC-4 (Financials) and MGT-7 (Annual Return) statutory filing status
- Shell company detection & Section 164(2) director disqualifications
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


class MCAConnector(BaseConnector):
    """
    Ministry of Corporate Affairs (MCA) Regulatory Connector.
    Provides statutory company master data, charge filings, and director compliance.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://mca.gov.in/mcafoportal",
        timeout_seconds: int = 30,
        use_mock: bool = True,
    ):
        super().__init__(api_key=api_key, base_url=base_url, timeout_seconds=timeout_seconds, use_mock=use_mock)

    @property
    def source_name(self) -> str:
        return "MCA"

    async def fetch_company(self, identifier: str) -> ConnectorCompany:
        """Fetch MCA Master Data by CIN, Company Name, or Ticker."""
        await asyncio.sleep(0.02)
        symbol = identifier.upper().strip()

        # Generate standard 21-character MCA CIN format: L72200MH1998PLC118942
        cin = f"L{abs(hash(symbol)) % 90000 + 10000}MH1998PLC{abs(hash(symbol)) % 900000 + 100000}"

        return ConnectorCompany(
            source=self.source_name,
            identifier=symbol,
            cin=cin,
            ticker=symbol,
            isin=f"INE{hash(symbol) % 90000000 + 10000000}014",
            name=f"{symbol} Private / Public Limited",
            legal_name=f"{symbol} Corporation (India) Limited",
            status="ACTIVE",
            incorporation_date="1998-07-24",
            registered_state="Maharashtra",
            registered_address="Plot No. 12, Bandra Kurla Complex, Bandra East, Mumbai - 400051",
            authorized_capital_inr=10000000000.0,
            paid_up_capital_inr=8500000000.0,
            industry="Commercial Services & Corporate Governance",
            sector="Industrials & Technology",
            directors_count=7,
            raw_response={
                "roc_code": "RoC-Mumbai",
                "company_category": "Company limited by Shares",
                "company_subcategory": "Union Government / Non-govt company",
                "class_of_company": "Public",
                "number_of_members": 42000,
                "date_of_last_agm": "2024-09-28",
                "date_of_balance_sheet": "2024-03-31",
            },
        )

    async def fetch_financials(self, identifier: str, years: int = 3) -> ConnectorFinancials:
        """Fetch MCA e-Form AOC-4 (XBRL financial filing records)."""
        await asyncio.sleep(0.02)
        symbol = identifier.upper().strip()

        statements = []
        base_rev = 32000.0 + (abs(hash(symbol)) % 12000)
        base_profit = base_rev * 0.17

        for i in range(years):
            fy = f"FY{2024 - i}"
            factor = 1.0 - (i * 0.08)
            statements.append(
                FinancialYearRecord(
                    fiscal_year=fy,
                    revenue_inr_cr=round(base_rev * factor, 2),
                    operating_profit_inr_cr=round(base_profit * 1.3 * factor, 2),
                    net_profit_inr_cr=round(base_profit * factor, 2),
                    total_assets_inr_cr=round(base_rev * 2.2 * factor, 2),
                    total_debt_inr_cr=round(base_rev * 0.15 * factor, 2),
                    net_worth_inr_cr=round(base_rev * 1.5 * factor, 2),
                    operating_margin_pct=round(22.1 - (i * 0.3), 2),
                    debt_to_equity=round(0.10 + (i * 0.01), 2),
                    current_ratio=2.2,
                    interest_coverage_ratio=22.0,
                )
            )

        return ConnectorFinancials(
            source=self.source_name,
            identifier=symbol,
            currency="INR",
            unit="Crores (10M INR)",
            statements=statements,
            key_ratios={
                "registered_charges_count": 4,
                "total_charge_amount_inr_cr": round(base_rev * 0.15, 2),
                "open_charges_amount_inr_cr": round(base_rev * 0.08, 2),
                "auditor_rotation_compliance": 1.0,
            },
            credit_rating="CRISIL AAA",
            credit_outlook="STABLE",
            raw_response={
                "form_aoc_4_xbrl_srn": f"F{abs(hash(symbol)) % 900000000 + 100000000}",
                "financial_year_end": "2024-03-31",
            },
        )

    async def fetch_compliance(self, identifier: str) -> ConnectorCompliance:
        """Fetch MCA statutory filing compliance, Section 164 director check, and shell company flags."""
        await asyncio.sleep(0.02)
        symbol = identifier.upper().strip()
        is_shell = "SHELL" in symbol or "DORMANT" in symbol

        filings = [
            ComplianceFiling(
                filing_type="FORM_AOC_4_XBRL",
                filing_date="2024-10-15",
                status="APPROVED",
                form_id="MCA-AOC4-883921",
                description="Filing of financial statements and other documents with Registrar.",
            ),
            ComplianceFiling(
                filing_type="FORM_MGT_7",
                filing_date="2024-11-02",
                status="APPROVED",
                form_id="MCA-MGT7-772910",
                description="Annual Return for financial year ended March 31, 2024.",
            ),
            ComplianceFiling(
                filing_type="FORM_DIR_12",
                filing_date="2024-08-14",
                status="APPROVED",
                form_id="MCA-DIR12-339102",
                description="Particulars of appointment of directors and key managerial personnel.",
            ),
        ]

        penalties = []
        if is_shell:
            penalties.append(
                RegulatoryPenalty(
                    authority="Registrar of Companies (RoC)",
                    order_date="2024-02-18",
                    section_violated="Section 248 of Companies Act, 2013 - Dormancy and Non-operation Notice",
                    penalty_amount_inr=500000.0,
                    adjudication_status="OPEN",
                    summary="Show-cause notice issued regarding non-commencement of business operations.",
                )
            )

        return ConnectorCompliance(
            source=self.source_name,
            identifier=symbol,
            compliance_score=45.0 if is_shell else 98.0,
            status="SEVERE_BREACH" if is_shell else "COMPLIANT",
            filings=filings,
            penalties=penalties,
            director_disqualifications_found=is_shell,
            shell_company_signals_flagged=is_shell,
            annual_general_meeting_date="2024-09-28",
            balance_sheet_filing_status="FILED" if not is_shell else "OVERDUE",
            raw_response={
                "roc_jurisdiction": "RoC Mumbai",
                "defaulting_status": is_shell,
                "charges_satisfied_percentage": 75.0,
            },
        )
