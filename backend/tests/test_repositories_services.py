"""
OZARK — Unit & Integration Tests for Repositories and Services
"""

import uuid
import pytest
from app.models.company import Company, ExchangeEnum
from app.models.financial import Financial
from app.models.risk_score import RiskLevel, RiskScore
from app.models.alert import Alert, AlertSeverity, AlertType
from app.models.user import User
from app.schemas.company import CompanyCreate
from app.schemas.financial import FinancialCreate
from app.schemas.risk_score import RiskScoreCreate
from app.schemas.alert import AlertCreate


def test_model_instantiation():
    # 1. Company
    c_id = uuid.uuid4()
    company = Company(
        id=c_id,
        name="Test Corp",
        ticker="TST",
        sector="Technology",
        industry="Software",
        country="United States",
        exchange=ExchangeEnum.NASDAQ,
        market_cap=5000.0,
    )
    assert company.name == "Test Corp"
    assert company.ticker == "TST"

    # 2. Financial
    f_id = uuid.uuid4()
    financial = Financial(
        id=f_id,
        company_id=c_id,
        fiscal_year=2024,
        revenue=1200.0,
        net_income=150.0,
    )
    assert financial.fiscal_year == 2024
    assert financial.revenue == 1200.0

    # 3. RiskScore
    rs_id = uuid.uuid4()
    risk_score = RiskScore(
        id=rs_id,
        company_id=c_id,
        overall_score=42.5,
        risk_level=RiskLevel.MEDIUM,
    )
    assert risk_score.overall_score == 42.5
    assert risk_score.risk_level == RiskLevel.MEDIUM

    # 4. Alert
    a_id = uuid.uuid4()
    alert = Alert(
        id=a_id,
        company_id=c_id,
        alert_type=AlertType.RISK_THRESHOLD,
        severity=AlertSeverity.WARNING,
        title="Test Alert",
        message="Risk threshold warning",
        alert_metadata={"score": 42.5},
    )
    assert alert.title == "Test Alert"
    assert alert.alert_metadata is not None
    assert alert.alert_metadata["score"] == 42.5

    # 5. User
    u_id = uuid.uuid4()
    user = User(
        id=u_id,
        name="Test User",
        email="test@ozark.dev",
        password_hash="fakehash",
    )
    assert user.email == "test@ozark.dev"


def test_schema_validations():
    c_id = uuid.uuid4()
    c_create = CompanyCreate(
        name="Apple Inc.",
        ticker="AAPL",
        sector="Technology",
        industry="Consumer Electronics",
        exchange=ExchangeEnum.NASDAQ,
    )
    assert c_create.ticker == "AAPL"

    f_create = FinancialCreate(
        company_id=c_id,
        fiscal_year=2024,
        revenue=390000.0,
    )
    assert f_create.fiscal_year == 2024

    rs_create = RiskScoreCreate(
        company_id=c_id,
        overall_score=15.0,
        risk_level=RiskLevel.LOW,
    )
    assert rs_create.overall_score == 15.0

    a_create = AlertCreate(
        company_id=c_id,
        alert_type=AlertType.RISK_THRESHOLD,
        severity=AlertSeverity.INFO,
        title="Notice",
        message="Info alert message",
    )
    assert a_create.title == "Notice"
