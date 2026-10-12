"""
OZARK Backend — Unit Tests for Data Connectors

Tests the common interface across:
- SEBIConnector
- MoneycontrolConnector
- ZerodhaConnector
- MCAConnector
- SMCConnector
- ConnectorRegistry
"""

import pytest

from app.connectors import (
    BaseConnector,
    ConnectorCompany,
    ConnectorCompliance,
    ConnectorFinancials,
    ConnectorRegistry,
    MCAConnector,
    MoneycontrolConnector,
    SEBIConnector,
    SMCConnector,
    ZerodhaConnector,
)


@pytest.mark.parametrize(
    "connector_cls,source_name",
    [
        (SEBIConnector, "SEBI"),
        (MoneycontrolConnector, "Moneycontrol"),
        (ZerodhaConnector, "Zerodha"),
        (MCAConnector, "MCA"),
        (SMCConnector, "SMC"),
    ],
)
@pytest.mark.asyncio
async def test_connector_common_interface(connector_cls, source_name):
    """Verify each connector implements the common interface methods with correct typing."""
    connector: BaseConnector = connector_cls(use_mock=True)

    # 1. Source name & Health Check
    assert connector.source_name == source_name
    health = await connector.health_check()
    assert health["source"] == source_name
    assert health["status"] == "HEALTHY"

    # 2. fetch_company()
    company = await connector.fetch_company("RELIANCE")
    assert isinstance(company, ConnectorCompany)
    assert company.source == source_name
    assert company.identifier == "RELIANCE"
    assert company.name is not None
    assert len(company.name) > 0
    assert company.status == "ACTIVE"

    # 3. fetch_financials()
    financials = await connector.fetch_financials("RELIANCE", years=3)
    assert isinstance(financials, ConnectorFinancials)
    assert financials.source == source_name
    assert financials.identifier == "RELIANCE"
    assert len(financials.statements) == 3
    for statement in financials.statements:
        assert statement.fiscal_year.startswith("FY")
        assert statement.revenue_inr_cr > 0
        assert statement.net_profit_inr_cr > 0

    # 4. fetch_compliance()
    compliance = await connector.fetch_compliance("RELIANCE")
    assert isinstance(compliance, ConnectorCompliance)
    assert compliance.source == source_name
    assert compliance.identifier == "RELIANCE"
    assert 0.0 <= compliance.compliance_score <= 100.0
    assert compliance.status in ["COMPLIANT", "DEFICIENT", "SEVERE_BREACH"]


@pytest.mark.asyncio
async def test_mca_shell_detection():
    """Verify MCA connector flags shell/dormant companies correctly."""
    mca = MCAConnector(use_mock=True)
    compliance = await mca.fetch_compliance("SHELL_CORP")
    assert compliance.shell_company_signals_flagged is True
    assert compliance.compliance_score < 50.0
    assert compliance.status == "SEVERE_BREACH"
    assert len(compliance.penalties) > 0


@pytest.mark.asyncio
async def test_sebi_penalty_tracking():
    """Verify SEBI connector returns adjudication penalties when flagged."""
    sebi = SEBIConnector(use_mock=True)
    compliance = await sebi.fetch_compliance("WARN_INC")
    assert compliance.status == "DEFICIENT"
    assert len(compliance.penalties) == 1
    assert compliance.penalties[0].authority == "SEBI Adjudication Division"


@pytest.mark.asyncio
async def test_connector_registry_aggregation():
    """Verify ConnectorRegistry can list, retrieve, and aggregate data in parallel."""
    connectors = ConnectorRegistry.list_connectors()
    assert set(connectors) == {"sebi", "moneycontrol", "zerodha", "mca", "smc"}

    profiles = await ConnectorRegistry.aggregate_company_profile("TCS")
    assert len(profiles) == 5
    assert "sebi" in profiles
    assert "moneycontrol" in profiles
    assert "zerodha" in profiles
    assert "mca" in profiles
    assert "smc" in profiles
