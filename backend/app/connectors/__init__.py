"""
OZARK Backend — Data Connectors Package

Exports:
- BaseConnector
- ConnectorCompany, ConnectorFinancials, ConnectorCompliance, FinancialYearRecord
- SEBIConnector (Securities and Exchange Board of India)
- MoneycontrolConnector (Consolidated Financials & Valuation)
- ZerodhaConnector (Kite Connect Quotes & Microstructure)
- MCAConnector (Ministry of Corporate Affairs CIN/DIN/Charges)
- SMCConnector (SMC Global Research & Credit Surveillance)
- ConnectorRegistry / ConnectorAggregator for unified multi-source orchestration
"""

from typing import Dict, List, Optional, Type
import asyncio

from app.connectors.base import (
    BaseConnector,
    ComplianceFiling,
    ConnectorCompany,
    ConnectorCompliance,
    ConnectorFinancials,
    FinancialYearRecord,
    RegulatoryPenalty,
)
from app.connectors.sebi_connector import SEBIConnector
from app.connectors.moneycontrol_connector import MoneycontrolConnector
from app.connectors.zerodha_connector import ZerodhaConnector
from app.connectors.mca_connector import MCAConnector
from app.connectors.smc_connector import SMCConnector


class ConnectorRegistry:
    """
    Central registry and aggregator for OZARK External Connectors.
    Allows easy registration, retrieval, and multi-source parallel data aggregation.
    """

    _connectors: Dict[str, BaseConnector] = {}

    @classmethod
    def initialize_default(cls, use_mock: bool = True) -> None:
        """Initialize all default system connectors in mock or live mode."""
        cls._connectors = {
            "sebi": SEBIConnector(use_mock=use_mock),
            "moneycontrol": MoneycontrolConnector(use_mock=use_mock),
            "zerodha": ZerodhaConnector(use_mock=use_mock),
            "mca": MCAConnector(use_mock=use_mock),
            "smc": SMCConnector(use_mock=use_mock),
        }

    @classmethod
    def get(cls, name: str) -> Optional[BaseConnector]:
        """Retrieve a registered connector by lowercase name."""
        if not cls._connectors:
            cls.initialize_default()
        return cls._connectors.get(name.lower())

    @classmethod
    def list_connectors(cls) -> List[str]:
        """Return list of available connector keys."""
        if not cls._connectors:
            cls.initialize_default()
        return list(cls._connectors.keys())

    @classmethod
    async def aggregate_company_profile(cls, identifier: str) -> Dict[str, ConnectorCompany]:
        """Fetch company profiles from all connectors in parallel."""
        if not cls._connectors:
            cls.initialize_default()

        tasks = {name: conn.fetch_company(identifier) for name, conn in cls._connectors.items()}
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        return {name: res for name, res in zip(tasks.keys(), results) if isinstance(res, ConnectorCompany)}

    @classmethod
    async def aggregate_compliance(cls, identifier: str) -> Dict[str, ConnectorCompliance]:
        """Fetch compliance records from all connectors in parallel."""
        if not cls._connectors:
            cls.initialize_default()

        tasks = {name: conn.fetch_compliance(identifier) for name, conn in cls._connectors.items()}
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        return {name: res for name, res in zip(tasks.keys(), results) if isinstance(res, ConnectorCompliance)}


__all__ = [
    "BaseConnector",
    "ConnectorCompany",
    "ConnectorFinancials",
    "ConnectorCompliance",
    "FinancialYearRecord",
    "ComplianceFiling",
    "RegulatoryPenalty",
    "SEBIConnector",
    "MoneycontrolConnector",
    "ZerodhaConnector",
    "MCAConnector",
    "SMCConnector",
    "ConnectorRegistry",
]
