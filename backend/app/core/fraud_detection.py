"""
OZARK — Fraud Detection Engine (fraud_detection.py)

Evaluates 5 primary forensic risk signals:
  1. Frequent Director / Executive Changes
  2. Negative Profit & Margin Deterioration Trend
  3. Accelerated Debt Growth & Excessive Leverage
  4. Regulatory Penalties & Legal Inquiries
  5. Possible Shell Company & Opaque Operations Signals

Returns:
  {
    "fraud_probability": float (0.0 - 1.0 or 0 - 100),
    "fraud_level": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
    "reasons": List[str],
    "signal_scores": Dict[str, Any]
  }
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class FraudLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    @classmethod
    def from_probability(cls, prob_score: float) -> "FraudLevel":
        if prob_score < 25.0:
            return cls.LOW
        elif prob_score < 50.0:
            return cls.MEDIUM
        elif prob_score < 75.0:
            return cls.HIGH
        else:
            return cls.CRITICAL


# ── Pydantic Input Schemas ────────────────────────────────────────────────────

class DirectorChangeSignal(BaseModel):
    director_changes_count: int = Field(
        default=0,
        ge=0,
        description="Number of board/C-suite changes in past 24 months",
    )
    cfo_or_auditor_resigned: bool = Field(
        default=False,
        description="Whether CFO or external auditing firm resigned abruptly",
    )


class ProfitTrendSignal(BaseModel):
    net_income_growth_pct: float = Field(
        default=0.0,
        description="YoY net income growth rate in % (e.g. -25.0 for 25% drop)",
    )
    operating_cash_flow_negative: bool = Field(
        default=False,
        description="Whether operating cash flow is negative despite positive net income",
    )
    consecutive_loss_quarters: int = Field(
        default=0,
        ge=0,
        description="Consecutive quarters with operating losses",
    )


class DebtGrowthSignal(BaseModel):
    debt_growth_pct: float = Field(
        default=0.0,
        description="YoY debt accumulation growth rate in %",
    )
    debt_to_equity_ratio: float = Field(
        default=0.5,
        ge=0,
        description="Debt to Equity ratio",
    )
    interest_coverage_ratio: Optional[float] = Field(
        default=4.0,
        description="EBIT / Interest Expense (lower = higher distress)",
    )


class RegulatoryPenaltySignal(BaseModel):
    penalty_count: int = Field(
        default=0,
        ge=0,
        description="Number of regulatory enforcement actions or fines in past 36 months",
    )
    total_fines_usd: float = Field(
        default=0.0,
        ge=0,
        description="Total monetary fines and sanctions ($ USD)",
    )
    active_sec_doj_investigation: bool = Field(
        default=False,
        description="Whether company is under active SEC/DOJ/regulatory investigation",
    )


class ShellCompanySignal(BaseModel):
    employee_count: Optional[int] = Field(
        default=100,
        description="Reported employee count",
    )
    annual_revenue_usd: Optional[float] = Field(
        default=50.0,
        description="Annual revenue in millions USD",
    )
    has_physical_headquarters: bool = Field(
        default=True,
        description="Whether company has verified physical operational office vs PO Box/shared workspace",
    )
    opaque_ownership_structure: bool = Field(
        default=False,
        description="Presence of layered offshore entities / nominee directors",
    )
    circular_revenue_transactions: bool = Field(
        default=False,
        description="Unexplained round-tripping transactions with related parties",
    )


class FraudDetectionInput(BaseModel):
    director_changes: Optional[DirectorChangeSignal] = None
    profit_trend: Optional[ProfitTrendSignal] = None
    debt_growth: Optional[DebtGrowthSignal] = None
    regulatory_penalties: Optional[RegulatoryPenaltySignal] = None
    shell_company: Optional[ShellCompanySignal] = None


class SignalBreakdown(BaseModel):
    score: float = Field(..., ge=0, le=100)
    severity: FraudLevel
    reasons: List[str]


class FraudDetectionResult(BaseModel):
    fraud_probability: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Aggregated fraud probability index (0.0 = clean, 100.0 = severe fraud anomaly)",
    )
    fraud_level: FraudLevel
    reasons: List[str]
    signal_scores: Optional[Dict[str, SignalBreakdown]] = None


# ── Detector Implementation ───────────────────────────────────────────────────

class FraudDetector:
    """
    Forensic fraud and corporate malfeasance detection engine.
    """

    # Signal Weights in composite fraud scoring
    WEIGHT_DIRECTOR_CHANGES = 0.20
    WEIGHT_PROFIT_TREND      = 0.20
    WEIGHT_DEBT_GROWTH       = 0.20
    WEIGHT_REGULATORY        = 0.20
    WEIGHT_SHELL_COMPANY     = 0.20

    @classmethod
    def evaluate(cls, signals: FraudDetectionInput) -> FraudDetectionResult:
        reasons: List[str] = []
        signal_scores: Dict[str, SignalBreakdown] = {}

        # 1. Frequent Director Changes Analysis
        dir_score, dir_reasons = cls._eval_director_changes(signals.director_changes)
        if dir_reasons:
            reasons.extend(dir_reasons)
        signal_scores["director_changes"] = SignalBreakdown(
            score=dir_score,
            severity=FraudLevel.from_probability(dir_score),
            reasons=dir_reasons,
        )

        # 2. Negative Profit Trend Analysis
        profit_score, profit_reasons = cls._eval_profit_trend(signals.profit_trend)
        if profit_reasons:
            reasons.extend(profit_reasons)
        signal_scores["profit_trend"] = SignalBreakdown(
            score=profit_score,
            severity=FraudLevel.from_probability(profit_score),
            reasons=profit_reasons,
        )

        # 3. High Debt Growth Analysis
        debt_score, debt_reasons = cls._eval_debt_growth(signals.debt_growth)
        if debt_reasons:
            reasons.extend(debt_reasons)
        signal_scores["debt_growth"] = SignalBreakdown(
            score=debt_score,
            severity=FraudLevel.from_probability(debt_score),
            reasons=debt_reasons,
        )

        # 4. Regulatory Penalties Analysis
        reg_score, reg_reasons = cls._eval_regulatory(signals.regulatory_penalties)
        if reg_reasons:
            reasons.extend(reg_reasons)
        signal_scores["regulatory_penalties"] = SignalBreakdown(
            score=reg_score,
            severity=FraudLevel.from_probability(reg_score),
            reasons=reg_reasons,
        )

        # 5. Possible Shell Company Signals Analysis
        shell_score, shell_reasons = cls._eval_shell_signals(signals.shell_company)
        if shell_reasons:
            reasons.extend(shell_reasons)
        signal_scores["shell_company_signals"] = SignalBreakdown(
            score=shell_score,
            severity=FraudLevel.from_probability(shell_score),
            reasons=shell_reasons,
        )

        # Compute composite weighted fraud score (0 to 100)
        composite_score = round(
            (dir_score * cls.WEIGHT_DIRECTOR_CHANGES)
            + (profit_score * cls.WEIGHT_PROFIT_TREND)
            + (debt_score * cls.WEIGHT_DEBT_GROWTH)
            + (reg_score * cls.WEIGHT_REGULATORY)
            + (shell_score * cls.WEIGHT_SHELL_COMPANY),
            2,
        )
        composite_score = max(0.0, min(100.0, composite_score))

        fraud_level = FraudLevel.from_probability(composite_score)

        if not reasons:
            reasons.append("Clean forensic audit trail. No anomalous governance, debt, or shell company patterns detected.")

        return FraudDetectionResult(
            fraud_probability=composite_score,
            fraud_level=fraud_level,
            reasons=reasons,
            signal_scores=signal_scores,
        )

    # ── Signal Evaluator Helpers ──────────────────────────────────────────────

    @staticmethod
    def _eval_director_changes(signal: Optional[DirectorChangeSignal]) -> tuple[float, List[str]]:
        if not signal:
            return 5.0, []

        score = 0.0
        reasons = []
        count = signal.director_changes_count

        if count >= 5:
            score += 60.0
            reasons.append(f"Frequent Director Changes: Severe board instability with {count} executive resignations/appointments within 24 months.")
        elif count >= 3:
            score += 35.0
            reasons.append(f"Frequent Director Changes: Elevated turnover with {count} executive transitions.")
        elif count >= 1:
            score += 10.0

        if signal.cfo_or_auditor_resigned:
            score += 40.0
            reasons.append("Frequent Director Changes: Sudden resignation of CFO or independent auditing firm detected.")

        return min(100.0, score), reasons

    @staticmethod
    def _eval_profit_trend(signal: Optional[ProfitTrendSignal]) -> tuple[float, List[str]]:
        if not signal:
            return 10.0, []

        score = 0.0
        reasons = []

        if signal.net_income_growth_pct <= -50.0:
            score += 45.0
            reasons.append(f"Negative Profit Trend: Severe earnings contraction ({signal.net_income_growth_pct:.1f}% YoY).")
        elif signal.net_income_growth_pct < -15.0:
            score += 25.0
            reasons.append(f"Negative Profit Trend: Negative earnings trajectory ({signal.net_income_growth_pct:.1f}% YoY).")

        if signal.operating_cash_flow_negative:
            score += 35.0
            reasons.append("Negative Profit Trend: Divergence anomaly — negative operating cash flow despite reported positive accounting net income.")

        if signal.consecutive_loss_quarters >= 4:
            score += 30.0
            reasons.append(f"Negative Profit Trend: Sustained operating losses across {signal.consecutive_loss_quarters} consecutive quarters.")

        return min(100.0, score), reasons

    @staticmethod
    def _eval_debt_growth(signal: Optional[DebtGrowthSignal]) -> tuple[float, List[str]]:
        if not signal:
            return 10.0, []

        score = 0.0
        reasons = []

        if signal.debt_growth_pct >= 60.0:
            score += 45.0
            reasons.append(f"High Debt Growth: Explosive debt accumulation (+{signal.debt_growth_pct:.1f}% YoY).")
        elif signal.debt_growth_pct >= 25.0:
            score += 25.0
            reasons.append(f"High Debt Growth: Above-average leverage acceleration (+{signal.debt_growth_pct:.1f}% YoY).")

        if signal.debt_to_equity_ratio >= 3.0:
            score += 35.0
            reasons.append(f"High Debt Growth: Overleveraged balance sheet with Debt-to-Equity ratio of {signal.debt_to_equity_ratio:.2f}x.")
        elif signal.debt_to_equity_ratio >= 1.8:
            score += 20.0

        if signal.interest_coverage_ratio is not None and signal.interest_coverage_ratio < 1.5:
            score += 25.0
            reasons.append(f"High Debt Growth: Inadequate interest coverage ({signal.interest_coverage_ratio:.2f}x EBIT coverage).")

        return min(100.0, score), reasons

    @staticmethod
    def _eval_regulatory(signal: Optional[RegulatoryPenaltySignal]) -> tuple[float, List[str]]:
        if not signal:
            return 0.0, []

        score = 0.0
        reasons = []

        if signal.penalty_count >= 3:
            score += 40.0
            reasons.append(f"Regulatory Penalties: Repeated regulatory non-compliance ({signal.penalty_count} enforcement actions).")
        elif signal.penalty_count >= 1:
            score += 20.0
            reasons.append(f"Regulatory Penalties: Past regulatory penalty recorded ({signal.penalty_count} action).")

        if signal.total_fines_usd >= 10_000_000:
            score += 30.0
            reasons.append(f"Regulatory Penalties: Material monetary sanctions exceeding ${(signal.total_fines_usd / 1_000_000):.1f}M USD.")
        elif signal.total_fines_usd > 500_000:
            score += 15.0

        if signal.active_sec_doj_investigation:
            score += 45.0
            reasons.append("Regulatory Penalties: Formal ongoing investigation by SEC / DOJ / Financial Conduct Authorities.")

        return min(100.0, score), reasons

    @staticmethod
    def _eval_shell_signals(signal: Optional[ShellCompanySignal]) -> tuple[float, List[str]]:
        if not signal:
            return 5.0, []

        score = 0.0
        reasons = []

        if not signal.has_physical_headquarters:
            score += 35.0
            reasons.append("Possible Shell Company Signals: No verifiable physical operational headquarters (virtual / PO Box / shared address).")

        if signal.opaque_ownership_structure:
            score += 35.0
            reasons.append("Possible Shell Company Signals: Opaque ownership structure with offshore shell intermediaries or nominee trustees.")

        if signal.circular_revenue_transactions:
            score += 40.0
            reasons.append("Possible Shell Company Signals: High risk of circular round-tripping transactions between undisclosed affiliated entities.")

        # Disproportionate revenue per employee
        if signal.employee_count is not None and signal.annual_revenue_usd is not None:
            if signal.employee_count <= 2 and signal.annual_revenue_usd > 10.0:
                score += 30.0
                reasons.append(f"Possible Shell Company Signals: Unrealistic revenue per head (${signal.annual_revenue_usd:.1f}M revenue with {signal.employee_count} employees).")

        return min(100.0, score), reasons
