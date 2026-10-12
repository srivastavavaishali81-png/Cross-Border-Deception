"""
OZARK — Risk Engine

Calculates composite risk scores using the weighted formula:
  - Financial Health:  25%
  - Compliance Score:  20%
  - Fraud Indicators:  20%
  - Market Stability:  15%
  - Network Risk:      10%
  - News Sentiment:     5%
  - Credit Rating:      5%

Output:
  {
    "risk_score": float (0–100),
    "risk_level": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
    "recommendation": str,
    ...
  }
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field, field_validator


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    @classmethod
    def from_score(cls, score: float) -> "RiskLevel":
        if score < 25.0:
            return cls.LOW
        elif score < 50.0:
            return cls.MEDIUM
        elif score < 75.0:
            return cls.HIGH
        else:
            return cls.CRITICAL


# ── Credit Rating Mapping ───────────────────────────────────────────────────────
CREDIT_RATING_RISK_MAP: Dict[str, float] = {
    "AAA": 5.0,
    "AA+": 8.0,
    "AA": 10.0,
    "AA-": 12.0,
    "A+": 15.0,
    "A": 18.0,
    "A-": 22.0,
    "BBB+": 28.0,
    "BBB": 35.0,
    "BBB-": 42.0,
    "BB+": 52.0,
    "BB": 60.0,
    "BB-": 68.0,
    "B+": 75.0,
    "B": 82.0,
    "B-": 88.0,
    "CCC+": 92.0,
    "CCC": 95.0,
    "CC": 98.0,
    "C": 99.0,
    "D": 100.0,
}


class RiskEngineInput(BaseModel):
    """
    Inputs for the OZARK Risk Engine.
    All numeric risk metrics are normalized to 0–100 scale unless otherwise noted.
    """
    financial_health: float = Field(
        ...,
        ge=0,
        le=100,
        description="Financial health score (0 = bankrupt/distressed, 100 = fortress balance sheet)",
    )
    compliance_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Regulatory & compliance score (0 = severe violations, 100 = full compliance)",
    )
    fraud_indicators: float = Field(
        ...,
        ge=0,
        le=100,
        description="Fraud / anomaly indicator index (0 = clean, 100 = high fraud probability)",
    )
    market_stability: float = Field(
        ...,
        ge=0,
        le=100,
        description="Market stability score (0 = extreme volatility, 100 = highly stable)",
    )
    network_risk: float = Field(
        ...,
        ge=0,
        le=100,
        description="Graph network / counterparty contagion risk (0 = isolated, 100 = systemic contagion)",
    )
    news_sentiment: Union[float, str] = Field(
        ...,
        description="News sentiment score (-1.0 to 1.0 or 0 to 100)",
    )
    credit_rating: Union[str, float] = Field(
        ...,
        description="Credit rating (e.g. 'AAA', 'BBB', 'BB') or numeric score (0–100)",
    )


from app.core.fraud_detection import (
    FraudDetector,
    FraudDetectionInput,
    FraudDetectionResult,
    FraudLevel,
)


class RiskComponentDetail(BaseModel):
    raw_input: Any
    normalized_risk: float
    weight: float
    weighted_contribution: float


class RiskEngineOutput(BaseModel):
    risk_score: float = Field(..., ge=0, le=100, description="Overall risk score (0-100, higher = riskier)")
    risk_level: RiskLevel
    recommendation: str
    breakdown: Optional[Dict[str, RiskComponentDetail]] = None
    fraud_detection: Optional[FraudDetectionResult] = None


class RiskEngine:
    """
    Calculates corporate risk scores based on weighted multi-dimensional factors.
    """

    # Weights defined in OZARK specifications
    WEIGHT_FINANCIAL_HEALTH = 0.25  # 25%
    WEIGHT_COMPLIANCE       = 0.20  # 20%
    WEIGHT_FRAUD_INDICATORS = 0.20  # 20%
    WEIGHT_MARKET_STABILITY = 0.15  # 15%
    WEIGHT_NETWORK_RISK     = 0.10  # 10%
    WEIGHT_NEWS_SENTIMENT   = 0.05  #  5%
    WEIGHT_CREDIT_RATING    = 0.05  #  5%

    @classmethod
    def _normalize_news_sentiment(cls, sentiment: Union[float, str]) -> float:
        """
        Converts news sentiment into a 0–100 risk score (higher = higher risk).
        If sentiment is in range [-1.0, +1.0]:
          +1.0 (very positive) -> 0 risk
           0.0 (neutral)       -> 50 risk
          -1.0 (very negative) -> 100 risk
        If already in [0, 100], scales accordingly.
        """
        try:
            val = float(sentiment)
            if -1.0 <= val <= 1.0:
                # Map [-1.0, 1.0] to [100, 0] risk
                return round((1.0 - val) * 50.0, 2)
            else:
                return round(max(0.0, min(100.0, 100.0 - val)), 2)
        except (ValueError, TypeError):
            sentiment_str = str(sentiment).upper()
            if "POS" in sentiment_str or "BULL" in sentiment_str:
                return 20.0
            elif "NEG" in sentiment_str or "BEAR" in sentiment_str:
                return 80.0
            return 50.0

    @classmethod
    def _normalize_credit_rating(cls, credit_rating: Union[str, float]) -> float:
        """
        Converts credit rating string (e.g. 'AAA', 'BBB-') or score to 0–100 risk score.
        """
        if isinstance(credit_rating, (int, float)):
            # If numeric: 100 = AAA (0 risk), 0 = D (100 risk)
            val = float(credit_rating)
            return round(max(0.0, min(100.0, 100.0 - val)), 2)

        rating_clean = str(credit_rating).strip().upper()
        if rating_clean in CREDIT_RATING_RISK_MAP:
            return CREDIT_RATING_RISK_MAP[rating_clean]

        # Check prefix match (e.g. 'AAA/STABLE' -> 'AAA')
        for k, v in CREDIT_RATING_RISK_MAP.items():
            if rating_clean.startswith(k):
                return v

        return 50.0  # Default investment-grade / average threshold

    @classmethod
    def calculate(
        cls,
        financial_health: float,
        compliance_score: float,
        fraud_indicators: Union[float, FraudDetectionInput, FraudDetectionResult],
        market_stability: float,
        network_risk: float,
        news_sentiment: Union[float, str],
        credit_rating: Union[str, float],
        include_breakdown: bool = True,
    ) -> RiskEngineOutput:
        """
        Execute weighted risk calculation with integrated fraud detection.
        """
        fraud_res: Optional[FraudDetectionResult] = None
        if isinstance(fraud_indicators, FraudDetectionResult):
            fraud_res = fraud_indicators
            fraud_val = fraud_res.fraud_probability
        elif isinstance(fraud_indicators, FraudDetectionInput):
            fraud_res = FraudDetector.evaluate(fraud_indicators)
            fraud_val = fraud_res.fraud_probability
        else:
            fraud_val = float(fraud_indicators)

        # 1. Transform inputs into risk dimensions (0–100, where 100 is maximum risk)
        # Financial Health: 100 health -> 0 risk
        fin_risk = max(0.0, min(100.0, 100.0 - float(financial_health)))

        # Compliance: 100 compliance -> 0 risk
        comp_risk = max(0.0, min(100.0, 100.0 - float(compliance_score)))

        # Fraud Indicators: 100 fraud -> 100 risk
        fraud_risk = max(0.0, min(100.0, float(fraud_val)))

        # Market Stability: 100 stability -> 0 risk
        mkt_risk = max(0.0, min(100.0, 100.0 - float(market_stability)))

        # Network Risk: 100 network risk -> 100 risk
        net_risk = max(0.0, min(100.0, float(network_risk)))

        # News Sentiment
        news_risk = cls._normalize_news_sentiment(news_sentiment)

        # Credit Rating
        credit_risk = cls._normalize_credit_rating(credit_rating)

        # 2. Weighted Sum
        w_fin = fin_risk * cls.WEIGHT_FINANCIAL_HEALTH
        w_comp = comp_risk * cls.WEIGHT_COMPLIANCE
        w_fraud = fraud_risk * cls.WEIGHT_FRAUD_INDICATORS
        w_mkt = mkt_risk * cls.WEIGHT_MARKET_STABILITY
        w_net = net_risk * cls.WEIGHT_NETWORK_RISK
        w_news = news_risk * cls.WEIGHT_NEWS_SENTIMENT
        w_credit = credit_risk * cls.WEIGHT_CREDIT_RATING

        total_score = round(
            w_fin + w_comp + w_fraud + w_mkt + w_net + w_news + w_credit, 2
        )
        total_score = max(0.0, min(100.0, total_score))

        # 3. Determine Risk Level
        risk_level = RiskLevel.from_score(total_score)

        # 4. Generate Institutional Recommendation
        recommendation = cls._generate_recommendation(
            total_score, risk_level, fin_risk, fraud_risk, comp_risk
        )

        breakdown = None
        if include_breakdown:
            breakdown = {
                "financial_health": RiskComponentDetail(
                    raw_input=financial_health,
                    normalized_risk=round(fin_risk, 2),
                    weight=cls.WEIGHT_FINANCIAL_HEALTH,
                    weighted_contribution=round(w_fin, 2),
                ),
                "compliance_score": RiskComponentDetail(
                    raw_input=compliance_score,
                    normalized_risk=round(comp_risk, 2),
                    weight=cls.WEIGHT_COMPLIANCE,
                    weighted_contribution=round(w_comp, 2),
                ),
                "fraud_indicators": RiskComponentDetail(
                    raw_input=fraud_indicators,
                    normalized_risk=round(fraud_risk, 2),
                    weight=cls.WEIGHT_FRAUD_INDICATORS,
                    weighted_contribution=round(w_fraud, 2),
                ),
                "market_stability": RiskComponentDetail(
                    raw_input=market_stability,
                    normalized_risk=round(mkt_risk, 2),
                    weight=cls.WEIGHT_MARKET_STABILITY,
                    weighted_contribution=round(w_mkt, 2),
                ),
                "network_risk": RiskComponentDetail(
                    raw_input=network_risk,
                    normalized_risk=round(net_risk, 2),
                    weight=cls.WEIGHT_NETWORK_RISK,
                    weighted_contribution=round(w_net, 2),
                ),
                "news_sentiment": RiskComponentDetail(
                    raw_input=news_sentiment,
                    normalized_risk=round(news_risk, 2),
                    weight=cls.WEIGHT_NEWS_SENTIMENT,
                    weighted_contribution=round(w_news, 2),
                ),
                "credit_rating": RiskComponentDetail(
                    raw_input=credit_rating,
                    normalized_risk=round(credit_risk, 2),
                    weight=cls.WEIGHT_CREDIT_RATING,
                    weighted_contribution=round(w_credit, 2),
                ),
            }

        return RiskEngineOutput(
            risk_score=total_score,
            risk_level=risk_level,
            recommendation=recommendation,
            breakdown=breakdown,
            fraud_detection=fraud_res,
        )

    @classmethod
    def _generate_recommendation(
        cls,
        score: float,
        level: RiskLevel,
        fin_risk: float,
        fraud_risk: float,
        comp_risk: float,
    ) -> str:
        if level == RiskLevel.LOW:
            return (
                "This company demonstrates strong financial stability and low fraud indicators. "
                "Approved for standard portfolio allocation with routine quarterly surveillance."
            )
        elif level == RiskLevel.MEDIUM:
            reasons = []
            if comp_risk > 30:
                reasons.append("moderate compliance risks")
            if fin_risk > 35:
                reasons.append("liquidity / leverage posture")
            if fraud_risk > 25:
                reasons.append("minor accounting signals")
            detail = f" due to {', '.join(reasons)}" if reasons else " due to moderate compliance risks"
            return (
                f"This investment requires caution{detail}. "
                "Heightened surveillance recommended; maintain current exposure limits without expansion."
            )
        elif level == RiskLevel.HIGH:
            return (
                "This company shows significant fraud indicators and weak financial health. "
                "Active risk mitigation required. Perform enhanced due diligence and hedge downside exposure."
            )
        else:  # CRITICAL
            return (
                "This company shows severe fraud indicators, critical governance violations, and highly distressed financial health. "
                "Immediate intervention required. Recommend capital preservation freeze and comprehensive forensic audit."
            )
