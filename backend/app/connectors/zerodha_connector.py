"""
OZARK Backend — Zerodha Kite Connect Data Connector

Connects to Zerodha Kite Connect trading & market data platform.
Specializes in:
- NSE/BSE real-time quotes, OHLCV candles, 52-week highs/lows
- Instrument tokens, trading symbol mapping, exchange segments
- Liquidity volume analysis & market volatility indicators
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
)


class ZerodhaConnector(BaseConnector):
    """
    Zerodha Kite Connect Market Data Connector.
    Provides mocked exchange quotes, market microstructure, and liquidity metrics.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        access_token: Optional[str] = None,
        base_url: str = "https://api.kite.trade",
        timeout_seconds: int = 15,
        use_mock: bool = True,
    ):
        super().__init__(api_key=api_key, base_url=base_url, timeout_seconds=timeout_seconds, use_mock=use_mock)
        self.access_token = access_token

    @property
    def source_name(self) -> str:
        return "Zerodha"

    async def fetch_company(self, identifier: str) -> ConnectorCompany:
        """Fetch Kite Connect instrument metadata, exchange scrip codes, and lot sizes."""
        await asyncio.sleep(0.02)
        symbol = identifier.upper().strip()

        return ConnectorCompany(
            source=self.source_name,
            identifier=symbol,
            ticker=symbol,
            isin=f"INE{hash(symbol) % 90000000 + 10000000}014",
            name=f"{symbol} Ltd",
            legal_name=f"{symbol} Limited (NSE Equities Segment)",
            status="ACTIVE",
            incorporation_date="2005-01-15",
            registered_state="Karnataka",
            registered_address="153/154, 4th Cross, Dollars Colony, JP Nagar 4th Phase, Bengaluru - 560078",
            authorized_capital_inr=2000000000.0,
            paid_up_capital_inr=1500000000.0,
            industry="Diversified Financials & Equity Markets",
            sector="Financial Services",
            directors_count=6,
            raw_response={
                "instrument_token": 738561 + (abs(hash(symbol)) % 50000),
                "exchange": "NSE",
                "tradingsymbol": symbol,
                "segment": "NSE_EQ",
                "tick_size": 0.05,
                "lot_size": 1,
            },
        )

    async def fetch_financials(self, identifier: str, years: int = 3) -> ConnectorFinancials:
        """Fetch trading turnover, market cap valuation, and annual fundamental ratios from Kite data."""
        await asyncio.sleep(0.02)
        symbol = identifier.upper().strip()

        statements = []
        base_rev = 18500.0 + (abs(hash(symbol)) % 8000)
        base_profit = base_rev * 0.15

        for i in range(years):
            fy = f"FY{2024 - i}"
            factor = 1.0 - (i * 0.07)
            statements.append(
                FinancialYearRecord(
                    fiscal_year=fy,
                    revenue_inr_cr=round(base_rev * factor, 2),
                    operating_profit_inr_cr=round(base_profit * 1.25 * factor, 2),
                    net_profit_inr_cr=round(base_profit * factor, 2),
                    total_assets_inr_cr=round(base_rev * 1.7 * factor, 2),
                    total_debt_inr_cr=round(base_rev * 0.18 * factor, 2),
                    net_worth_inr_cr=round(base_rev * 1.35 * factor, 2),
                    operating_margin_pct=round(21.0 - (i * 0.6), 2),
                    debt_to_equity=round(0.14 + (i * 0.01), 2),
                    current_ratio=2.1,
                    interest_coverage_ratio=18.0,
                )
            )

        last_price = 2450.0 + (abs(hash(symbol)) % 1500)
        return ConnectorFinancials(
            source=self.source_name,
            identifier=symbol,
            currency="INR",
            unit="Crores (10M INR)",
            statements=statements,
            key_ratios={
                "last_traded_price_inr": round(last_price, 2),
                "day_high_inr": round(last_price * 1.025, 2),
                "day_low_inr": round(last_price * 0.985, 2),
                "52_week_high_inr": round(last_price * 1.25, 2),
                "52_week_low_inr": round(last_price * 0.72, 2),
                "average_daily_volume": 1420500,
                "beta_volatility": 1.12,
            },
            credit_rating="CARE AAA",
            credit_outlook="STABLE",
            raw_response={"market_depth_spread_bps": 2.4, "circuit_limit_pct": 20.0},
        )

    async def fetch_compliance(self, identifier: str) -> ConnectorCompliance:
        """Fetch Kite surveillance alerts (ASM / GSM framework, Circuit Breakers)."""
        await asyncio.sleep(0.02)
        symbol = identifier.upper().strip()
        is_asm = "ASM" in symbol

        return ConnectorCompliance(
            source=self.source_name,
            identifier=symbol,
            compliance_score=60.0 if is_asm else 96.0,
            status="DEFICIENT" if is_asm else "COMPLIANT",
            filings=[
                ComplianceFiling(
                    filing_type="EXCHANGE_SURVEILLANCE_CHECK",
                    filing_date="2024-10-08",
                    status="APPROVED",
                    description="Standard exchange risk management surveillance criteria satisfied.",
                )
            ],
            penalties=[],
            director_disqualifications_found=False,
            shell_company_signals_flagged=False,
            annual_general_meeting_date="2024-09-10",
            balance_sheet_filing_status="FILED",
            raw_response={
                "in_asm_list": is_asm,
                "in_gsm_list": False,
                "margin_multiplier": 1.0,
            },
        )
