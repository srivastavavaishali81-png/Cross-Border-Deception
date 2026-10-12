"""
OZARK Backend — Company Endpoints

Provides endpoints:
- GET /companies (and /api/v1/companies): List with filtering by industry, state, company name, sorting & pagination
- GET /companies/search (and /api/v1/companies/search): Full-text / fuzzy search by query `q`
- GET /companies/filters (and /api/v1/companies/filters): Metadata for filter dropdowns
- GET /companies/{id} (and /api/v1/companies/{id}): Company details with financials, risk score, alerts
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.company import (
    CompanyDetail,
    CompanyListResponse,
    CompanySearchResponse,
    FilterOptions,
)
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])


# ── Metadata & Filters ────────────────────────────────────────────────────────

@router.get(
    "/filters",
    response_model=FilterOptions,
    summary="Get filter options",
    description="Returns distinct lists of industries, states, sectors, and risk levels for filtering.",
)
async def get_filter_options():
    return CompanyService.get_filter_options()


# ── Search ────────────────────────────────────────────────────────────────────

@router.get(
    "/search",
    response_model=CompanySearchResponse,
    summary="Search companies",
    description="Search companies by free-text query `q` (matching name, ticker, industry, state, etc.) with optional filtering.",
)
async def search_companies(
    q: Optional[str] = Query(default="", description="Search query string"),
    industry: Optional[str] = Query(default=None, description="Filter by industry"),
    state: Optional[str] = Query(default=None, description="Filter by US state code (e.g. CA, NY, TX)"),
    name: Optional[str] = Query(default=None, description="Filter by company name substring"),
    sector: Optional[str] = Query(default=None, description="Filter by sector"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=12, ge=1, le=100, description="Items per page"),
):
    return CompanyService.search_companies(
        query=q or "",
        industry=industry,
        state=state,
        name=name,
        sector=sector,
        page=page,
        page_size=page_size,
    )


# ── List & Filter ─────────────────────────────────────────────────────────────

@router.get(
    "",
    response_model=CompanyListResponse,
    summary="List and filter companies",
    description="List companies with filtering by Industry, State, Company Name, and sorting options.",
)
async def list_companies(
    industry: Optional[str] = Query(default=None, description="Filter by industry"),
    state: Optional[str] = Query(default=None, description="Filter by US state code (e.g. CA, NY, TX)"),
    name: Optional[str] = Query(default=None, description="Filter by company name"),
    sector: Optional[str] = Query(default=None, description="Filter by sector"),
    risk_level: Optional[str] = Query(default=None, description="Filter by risk level (LOW, MEDIUM, HIGH, CRITICAL)"),
    sort_by: str = Query(default="market_cap", description="Field to sort by (market_cap, name, founded_year, risk_score)"),
    sort_order: str = Query(default="desc", description="Sort direction (asc, desc)"),
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=12, ge=1, le=100, description="Items per page"),
):
    return CompanyService.list_companies(
        industry=industry,
        state=state,
        name=name,
        sector=sector,
        risk_level=risk_level,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )


# ── Company Details ───────────────────────────────────────────────────────────

@router.get(
    "/{id}",
    response_model=CompanyDetail,
    summary="Get company details by ID or ticker",
    description="Retrieve comprehensive company profile, financials history, risk score analysis, and alerts.",
)
async def get_company_details(id: str):
    company = CompanyService.get_company_by_id(id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company '{id}' was not found.",
        )
    return company


# ── Company Risk Engine Evaluation ────────────────────────────────────────────

@router.get(
    "/{id}/risk",
    summary="Calculate 7-factor weighted risk engine score",
    description=(
        "Executes the OZARK Risk Engine for a company using the weighted formula:\n"
        "- Financial Health: 25%\n"
        "- Compliance: 20%\n"
        "- Fraud Indicators: 20%\n"
        "- Market Stability: 15%\n"
        "- Network Risk: 10%\n"
        "- News Sentiment: 5%\n"
        "- Credit Rating: 5%\n\n"
        "Returns risk_score, risk_level, recommendation, and detailed component breakdown. "
        "Allows query parameter overrides for scenario stress-testing."
    ),
)
async def evaluate_company_risk(
    id: str,
    financial_health: Optional[float] = Query(default=None, ge=0, le=100, description="Override Financial Health (0-100)"),
    compliance_score: Optional[float] = Query(default=None, ge=0, le=100, description="Override Compliance Score (0-100)"),
    fraud_indicators: Optional[float] = Query(default=None, ge=0, le=100, description="Override Fraud Indicators (0-100)"),
    market_stability: Optional[float] = Query(default=None, ge=0, le=100, description="Override Market Stability (0-100)"),
    network_risk: Optional[float] = Query(default=None, ge=0, le=100, description="Override Network Risk (0-100)"),
    news_sentiment: Optional[float] = Query(default=None, description="Override News Sentiment (-1.0 to 1.0 or 0-100)"),
    credit_rating: Optional[str] = Query(default=None, description="Override Credit Rating (e.g. 'AAA', 'A', 'BBB')"),
):
    from app.core.risk_engine import RiskEngine

    company = CompanyService.get_company_by_id(id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company '{id}' was not found.",
        )

    # Derive baseline factor values from company profile if not explicitly overridden
    latest_risk = company.latest_risk_score or (company.risk_scores[0] if company.risk_scores else None)

    # Base financial health (inverse of credit risk or default based on score)
    fin_h = financial_health if financial_health is not None else (
        max(10.0, 100.0 - (latest_risk.credit_risk * 1.5 if latest_risk and latest_risk.credit_risk else 20.0))
    )

    # Compliance score
    comp_s = compliance_score if compliance_score is not None else (
        max(20.0, 100.0 - (latest_risk.operational_risk * 0.8 if latest_risk and latest_risk.operational_risk else 15.0))
    )

    # Fraud indicators
    fraud_i = fraud_indicators if fraud_indicators is not None else (
        min(80.0, (latest_risk.operational_risk * 0.4 if latest_risk and latest_risk.operational_risk else 5.0))
    )

    # Market stability
    mkt_s = market_stability if market_stability is not None else (
        max(15.0, 100.0 - (latest_risk.market_risk * 1.2 if latest_risk and latest_risk.market_risk else 25.0))
    )

    # Network risk
    net_r = network_risk if network_risk is not None else (
        min(75.0, (latest_risk.liquidity_risk * 0.9 if latest_risk and latest_risk.liquidity_risk else 15.0))
    )

    # News sentiment
    sentiment_val = news_sentiment if news_sentiment is not None else (
        0.65 if (latest_risk and latest_risk.overall_score < 30) else (
            -0.25 if (latest_risk and latest_risk.overall_score > 50) else 0.10
        )
    )

    # Credit rating
    rating_val = credit_rating if credit_rating is not None else (
        "AAA" if (latest_risk and latest_risk.overall_score < 15) else (
            "AA" if (latest_risk and latest_risk.overall_score < 25) else (
                "A" if (latest_risk and latest_risk.overall_score < 35) else (
                    "BBB" if (latest_risk and latest_risk.overall_score < 50) else "BB"
                )
            )
        )
    )

    # Execute Risk Engine calculation
    result = RiskEngine.calculate(
        financial_health=fin_h,
        compliance_score=comp_s,
        fraud_indicators=fraud_i,
        market_stability=mkt_s,
        network_risk=net_r,
        news_sentiment=sentiment_val,
        credit_rating=rating_val,
        include_breakdown=True,
    )

    return {
        "company_id": str(company.id),
        "ticker": company.ticker,
        "name": company.name,
        "risk_score": result.risk_score,
        "risk_level": result.risk_level.value,
        "recommendation": result.recommendation,
        "formula_weights": {
            "financial_health": "25%",
            "compliance": "20%",
            "fraud_indicators": "20%",
            "market_stability": "15%",
            "network_risk": "10%",
            "news_sentiment": "5%",
            "credit_rating": "5%",
        },
        "breakdown": {
            k: {
                "raw_input": v.raw_input,
                "normalized_risk_score": v.normalized_risk,
                "weight_percent": f"{int(v.weight * 100)}%",
                "weighted_contribution": v.weighted_contribution,
            }
            for k, v in (result.breakdown or {}).items()
        },
    }


# ── Fraud Detection Evaluation ────────────────────────────────────────────────

@router.get(
    "/{id}/fraud",
    summary="Detect fraud and forensic corporate anomalies",
    description=(
        "Executes OZARK Fraud Detection for a company across 5 forensic risk signals:\n"
        "1. Frequent Director Changes\n"
        "2. Negative Profit Trend\n"
        "3. High Debt Growth\n"
        "4. Regulatory Penalties\n"
        "5. Possible Shell Company Signals"
    ),
)
async def evaluate_company_fraud(
    id: str,
    director_changes: Optional[int] = Query(default=None, ge=0, description="Director changes in 24 months"),
    cfo_resigned: Optional[bool] = Query(default=None, description="CFO or auditor resigned abruptly"),
    net_income_growth_pct: Optional[float] = Query(default=None, description="YoY net income growth in %"),
    debt_growth_pct: Optional[float] = Query(default=None, description="YoY debt accumulation growth in %"),
    penalty_count: Optional[int] = Query(default=None, ge=0, description="Regulatory penalties recorded"),
    active_investigation: Optional[bool] = Query(default=None, description="Active SEC/DOJ inquiry"),
    no_physical_hq: Optional[bool] = Query(default=None, description="Virtual / shared / missing HQ"),
):
    from app.core.fraud_detection import (
        FraudDetector,
        FraudDetectionInput,
        DirectorChangeSignal,
        ProfitTrendSignal,
        DebtGrowthSignal,
        RegulatoryPenaltySignal,
        ShellCompanySignal,
    )

    company = CompanyService.get_company_by_id(id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company '{id}' was not found.",
        )

    # Derive baseline company financial metrics
    latest_fin = company.financials[0] if company.financials else None
    latest_risk = company.latest_risk_score or (company.risk_scores[0] if company.risk_scores else None)

    # Build detection input
    input_signals = FraudDetectionInput(
        director_changes=DirectorChangeSignal(
            director_changes_count=director_changes if director_changes is not None else (
                4 if latest_risk and latest_risk.overall_score > 55 else 1
            ),
            cfo_or_auditor_resigned=cfo_resigned if cfo_resigned is not None else (
                True if latest_risk and latest_risk.overall_score > 70 else False
            ),
        ),
        profit_trend=ProfitTrendSignal(
            net_income_growth_pct=net_income_growth_pct if net_income_growth_pct is not None else (
                -35.0 if latest_risk and latest_risk.overall_score > 50 else 12.5
            ),
            operating_cash_flow_negative=False if latest_fin and latest_fin.operating_cash_flow and latest_fin.operating_cash_flow > 0 else False,
            consecutive_loss_quarters=2 if latest_risk and latest_risk.overall_score > 60 else 0,
        ),
        debt_growth=DebtGrowthSignal(
            debt_growth_pct=debt_growth_pct if debt_growth_pct is not None else (
                45.0 if latest_risk and latest_risk.overall_score > 50 else 8.0
            ),
            debt_to_equity_ratio=float(latest_fin.debt_to_equity) if latest_fin and latest_fin.debt_to_equity else 0.45,
            interest_coverage_ratio=2.1 if latest_risk and latest_risk.overall_score > 50 else 8.5,
        ),
        regulatory_penalties=RegulatoryPenaltySignal(
            penalty_count=penalty_count if penalty_count is not None else (
                2 if latest_risk and latest_risk.overall_score > 65 else 0
            ),
            total_fines_usd=2500000.0 if latest_risk and latest_risk.overall_score > 65 else 0.0,
            active_sec_doj_investigation=active_investigation if active_investigation is not None else (
                True if latest_risk and latest_risk.overall_score > 75 else False
            ),
        ),
        shell_company=ShellCompanySignal(
            employee_count=company.employees or 100,
            annual_revenue_usd=latest_fin.revenue if latest_fin and latest_fin.revenue else 100.0,
            has_physical_headquarters=not no_physical_hq if no_physical_hq is not None else True,
            opaque_ownership_structure=False,
            circular_revenue_transactions=False,
        ),
    )

    result = FraudDetector.evaluate(input_signals)

    return {
        "company_id": str(company.id),
        "ticker": company.ticker,
        "name": company.name,
        "fraud_probability": result.fraud_probability,
        "fraud_level": result.fraud_level.value,
        "reasons": result.reasons,
        "signal_scores": {
            k: {
                "score": v.score,
                "severity": v.severity.value,
                "reasons": v.reasons,
            }
            for k, v in (result.signal_scores or {}).items()
        },
    }


