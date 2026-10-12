"""
OZARK — Unit Tests for risk_engine.py
"""

import pytest
from app.core.risk_engine import (
    RiskEngine,
    RiskEngineInput,
    RiskEngineOutput,
    RiskLevel,
    CREDIT_RATING_RISK_MAP,
)


def test_weights_sum_to_one():
    total_weights = (
        RiskEngine.WEIGHT_FINANCIAL_HEALTH
        + RiskEngine.WEIGHT_COMPLIANCE
        + RiskEngine.WEIGHT_FRAUD_INDICATORS
        + RiskEngine.WEIGHT_MARKET_STABILITY
        + RiskEngine.WEIGHT_NETWORK_RISK
        + RiskEngine.WEIGHT_NEWS_SENTIMENT
        + RiskEngine.WEIGHT_CREDIT_RATING
    )
    assert pytest.approx(total_weights, 0.001) == 1.00


def test_pristine_company_calculation():
    # Pristine blue-chip company:
    # 100 Financial Health, 100 Compliance, 0 Fraud, 100 Market Stability, 0 Network Risk, 1.0 Positive News, "AAA"
    output = RiskEngine.calculate(
        financial_health=100.0,
        compliance_score=100.0,
        fraud_indicators=0.0,
        market_stability=100.0,
        network_risk=0.0,
        news_sentiment=1.0,
        credit_rating="AAA",
    )

    assert isinstance(output, RiskEngineOutput)
    assert output.risk_score < 10.0
    assert output.risk_level == RiskLevel.LOW
    assert "Approved for standard portfolio allocation" in output.recommendation
    assert output.breakdown is not None
    assert "financial_health" in output.breakdown


def test_distressed_company_calculation():
    # Highly distressed company:
    # 10 Financial Health, 20 Compliance, 90 Fraud, 15 Market Stability, 85 Network Risk, -0.9 Negative News, "CCC"
    output = RiskEngine.calculate(
        financial_health=10.0,
        compliance_score=20.0,
        fraud_indicators=90.0,
        market_stability=15.0,
        network_risk=85.0,
        news_sentiment=-0.9,
        credit_rating="CCC",
    )

    assert output.risk_score >= 75.0
    assert output.risk_level == RiskLevel.CRITICAL
    assert "Immediate intervention required" in output.recommendation


def test_medium_risk_calculation():
    output = RiskEngine.calculate(
        financial_health=65.0,
        compliance_score=70.0,
        fraud_indicators=20.0,
        market_stability=60.0,
        network_risk=25.0,
        news_sentiment=0.1,
        credit_rating="BBB",
    )

    assert 25.0 <= output.risk_score < 50.0
    assert output.risk_level == RiskLevel.MEDIUM


def test_credit_rating_normalization():
    assert RiskEngine._normalize_credit_rating("AAA") == 5.0
    assert RiskEngine._normalize_credit_rating("BBB") == 35.0
    assert RiskEngine._normalize_credit_rating("D") == 100.0
    assert RiskEngine._normalize_credit_rating(85.0) == 15.0


def test_news_sentiment_normalization():
    # +1.0 -> 0 risk
    assert RiskEngine._normalize_news_sentiment(1.0) == 0.0
    # -1.0 -> 100 risk
    assert RiskEngine._normalize_news_sentiment(-1.0) == 100.0
    # 0.0 -> 50 risk
    assert RiskEngine._normalize_news_sentiment(0.0) == 50.0


def test_natural_language_recommendation_examples():
    # Low Risk example
    low_out = RiskEngine.calculate(
        financial_health=95.0,
        compliance_score=95.0,
        fraud_indicators=5.0,
        market_stability=90.0,
        network_risk=5.0,
        news_sentiment=0.8,
        credit_rating="AAA",
    )
    assert low_out.risk_level == RiskLevel.LOW
    assert "This company demonstrates strong financial stability and low fraud indicators." in low_out.recommendation

    # Medium Risk example
    med_out = RiskEngine.calculate(
        financial_health=65.0,
        compliance_score=55.0,
        fraud_indicators=25.0,
        market_stability=60.0,
        network_risk=30.0,
        news_sentiment=0.0,
        credit_rating="BBB",
    )
    assert med_out.risk_level == RiskLevel.MEDIUM
    assert "This investment requires caution" in med_out.recommendation
    assert "moderate compliance risks" in med_out.recommendation

    # High Risk example
    high_out = RiskEngine.calculate(
        financial_health=35.0,
        compliance_score=40.0,
        fraud_indicators=70.0,
        market_stability=40.0,
        network_risk=65.0,
        news_sentiment=-0.5,
        credit_rating="B",
    )
    assert high_out.risk_level == RiskLevel.HIGH
    assert "This company shows significant fraud indicators and weak financial health." in high_out.recommendation

