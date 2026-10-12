"""
OZARK — Unit Tests for fraud_detection.py and integration with risk_engine.py
"""

import pytest
from app.core.fraud_detection import (
    FraudDetector,
    FraudDetectionInput,
    FraudDetectionResult,
    FraudLevel,
    DirectorChangeSignal,
    ProfitTrendSignal,
    DebtGrowthSignal,
    RegulatoryPenaltySignal,
    ShellCompanySignal,
)
from app.core.risk_engine import RiskEngine, RiskLevel


def test_clean_company_fraud_evaluation():
    # Pristine company with clean signals
    signals = FraudDetectionInput(
        director_changes=DirectorChangeSignal(director_changes_count=0, cfo_or_auditor_resigned=False),
        profit_trend=ProfitTrendSignal(net_income_growth_pct=15.0, operating_cash_flow_negative=False),
        debt_growth=DebtGrowthSignal(debt_growth_pct=5.0, debt_to_equity_ratio=0.3),
        regulatory_penalties=RegulatoryPenaltySignal(penalty_count=0, total_fines_usd=0.0),
        shell_company=ShellCompanySignal(employee_count=5000, annual_revenue_usd=1200.0, has_physical_headquarters=True),
    )

    result = FraudDetector.evaluate(signals)
    assert isinstance(result, FraudDetectionResult)
    assert result.fraud_probability < 20.0
    assert result.fraud_level == FraudLevel.LOW
    assert "Clean forensic audit trail" in result.reasons[0]


def test_high_fraud_signals_detection():
    # Highly suspicious anomaly company
    signals = FraudDetectionInput(
        director_changes=DirectorChangeSignal(director_changes_count=6, cfo_or_auditor_resigned=True),
        profit_trend=ProfitTrendSignal(net_income_growth_pct=-65.0, operating_cash_flow_negative=True),
        debt_growth=DebtGrowthSignal(debt_growth_pct=85.0, debt_to_equity_ratio=4.5),
        regulatory_penalties=RegulatoryPenaltySignal(penalty_count=4, total_fines_usd=15_000_000.0, active_sec_doj_investigation=True),
        shell_company=ShellCompanySignal(employee_count=1, annual_revenue_usd=85.0, has_physical_headquarters=False, circular_revenue_transactions=True),
    )

    result = FraudDetector.evaluate(signals)
    assert result.fraud_probability >= 75.0
    assert result.fraud_level == FraudLevel.CRITICAL
    assert len(result.reasons) >= 5
    assert any("Frequent Director Changes" in r for r in result.reasons)
    assert any("Negative Profit Trend" in r for r in result.reasons)
    assert any("High Debt Growth" in r for r in result.reasons)
    assert any("Regulatory Penalties" in r for r in result.reasons)
    assert any("Possible Shell Company Signals" in r for r in result.reasons)


def test_risk_engine_integration_with_fraud_signals():
    # Pass FraudDetectionInput directly into RiskEngine.calculate
    fraud_signals = FraudDetectionInput(
        director_changes=DirectorChangeSignal(director_changes_count=5, cfo_or_auditor_resigned=True),
        profit_trend=ProfitTrendSignal(net_income_growth_pct=-55.0, operating_cash_flow_negative=True),
        debt_growth=DebtGrowthSignal(debt_growth_pct=70.0, debt_to_equity_ratio=3.8),
        regulatory_penalties=RegulatoryPenaltySignal(penalty_count=3, active_sec_doj_investigation=True),
        shell_company=ShellCompanySignal(employee_count=2, annual_revenue_usd=45.0, has_physical_headquarters=False),
    )

    risk_output = RiskEngine.calculate(
        financial_health=25.0,
        compliance_score=30.0,
        fraud_indicators=fraud_signals,
        market_stability=35.0,
        network_risk=60.0,
        news_sentiment=-0.8,
        credit_rating="B-",
    )

    assert risk_output.fraud_detection is not None
    assert risk_output.fraud_detection.fraud_level in [FraudLevel.HIGH, FraudLevel.CRITICAL]
    assert risk_output.risk_score >= 60.0
    assert risk_output.breakdown is not None
    assert "fraud_indicators" in risk_output.breakdown
    assert risk_output.breakdown["fraud_indicators"].weighted_contribution > 10.0
