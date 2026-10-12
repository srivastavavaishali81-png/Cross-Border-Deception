"""create companies, financials, risk_scores, alerts tables

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-09
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

exchange_enum = sa.Enum("NYSE", "NASDAQ", "LSE", "TSX", "ASX", "HKEX", "OTHER", name="exchange_enum")
risk_level_enum = sa.Enum("LOW", "MEDIUM", "HIGH", "CRITICAL", name="risk_level_enum")
alert_type_enum = sa.Enum("RISK_THRESHOLD", "PRICE_MOVEMENT", "EARNINGS", "REGULATORY", "CUSTOM", name="alert_type_enum")
alert_severity_enum = sa.Enum("INFO", "WARNING", "ERROR", "CRITICAL", name="alert_severity_enum")


def upgrade() -> None:
    # ── 1. Create Companies Table ─────────────────────────────────────────────
    op.create_table(
        "companies",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("ticker", sa.String(20), nullable=False),
        sa.Column("sector", sa.String(100), nullable=False),
        sa.Column("industry", sa.String(100), nullable=False),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("state", sa.String(100), nullable=True),
        sa.Column("city", sa.String(100), nullable=True),
        sa.Column("exchange", exchange_enum, nullable=False),
        sa.Column("market_cap", sa.Numeric(20, 2), nullable=True, comment="Market cap in millions USD"),
        sa.Column("employees", sa.Integer(), nullable=True),
        sa.Column("founded_year", sa.Integer(), nullable=True),
        sa.Column("website", sa.String(255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.UniqueConstraint("ticker", name="uq_companies_ticker"),
    )
    op.create_index("ix_companies_id", "companies", ["id"])
    op.create_index("ix_companies_name", "companies", ["name"])
    op.create_index("ix_companies_ticker", "companies", ["ticker"])
    op.create_index("ix_companies_sector", "companies", ["sector"])
    op.create_index("ix_companies_country", "companies", ["country"])
    op.create_index("ix_companies_state", "companies", ["state"])

    # ── 2. Create Financials Table ────────────────────────────────────────────
    op.create_table(
        "financials",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "company_id",
            UUID(as_uuid=True),
            sa.ForeignKey("companies.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("fiscal_year", sa.Integer(), nullable=False),
        sa.Column("fiscal_quarter", sa.Integer(), nullable=True),
        sa.Column("revenue", sa.Numeric(20, 2), nullable=True),
        sa.Column("gross_profit", sa.Numeric(20, 2), nullable=True),
        sa.Column("ebitda", sa.Numeric(20, 2), nullable=True),
        sa.Column("net_income", sa.Numeric(20, 2), nullable=True),
        sa.Column("eps", sa.Numeric(10, 4), nullable=True),
        sa.Column("total_assets", sa.Numeric(20, 2), nullable=True),
        sa.Column("total_debt", sa.Numeric(20, 2), nullable=True),
        sa.Column("cash_and_equivalents", sa.Numeric(20, 2), nullable=True),
        sa.Column("operating_cash_flow", sa.Numeric(20, 2), nullable=True),
        sa.Column("capex", sa.Numeric(20, 2), nullable=True),
        sa.Column("pe_ratio", sa.Numeric(10, 2), nullable=True),
        sa.Column("debt_to_equity", sa.Numeric(10, 4), nullable=True),
        sa.Column("current_ratio", sa.Numeric(10, 4), nullable=True),
        sa.Column("reported_at", sa.Date(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.UniqueConstraint(
            "company_id", "fiscal_year", "fiscal_quarter",
            name="uq_financials_company_period"
        ),
    )
    op.create_index("ix_financials_id", "financials", ["id"])
    op.create_index("ix_financials_company_id", "financials", ["company_id"])
    op.create_index("ix_financials_fiscal_year", "financials", ["fiscal_year"])

    # ── 3. Create Risk Scores Table ───────────────────────────────────────────
    op.create_table(
        "risk_scores",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "company_id",
            UUID(as_uuid=True),
            sa.ForeignKey("companies.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("overall_score", sa.Numeric(5, 2), nullable=False, comment="0-100"),
        sa.Column("risk_level", risk_level_enum, nullable=False),
        sa.Column("credit_risk", sa.Numeric(5, 2), nullable=True),
        sa.Column("market_risk", sa.Numeric(5, 2), nullable=True),
        sa.Column("operational_risk", sa.Numeric(5, 2), nullable=True),
        sa.Column("liquidity_risk", sa.Numeric(5, 2), nullable=True),
        sa.Column("esg_score", sa.Numeric(5, 2), nullable=True, comment="ESG score (higher = better ESG)"),
        sa.Column("model_version", sa.String(50), server_default="v1.0.0", nullable=False),
        sa.Column(
            "calculated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index("ix_risk_scores_id", "risk_scores", ["id"])
    op.create_index("ix_risk_scores_company_id", "risk_scores", ["company_id"])
    op.create_index("ix_risk_scores_risk_level", "risk_scores", ["risk_level"])
    op.create_index("ix_risk_scores_calculated_at", "risk_scores", ["calculated_at"])

    # ── 4. Create Alerts Table ────────────────────────────────────────────────
    op.create_table(
        "alerts",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "company_id",
            UUID(as_uuid=True),
            sa.ForeignKey("companies.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("alert_type", alert_type_enum, nullable=False),
        sa.Column("severity", alert_severity_enum, nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("is_read", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("is_resolved", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", JSONB, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index("ix_alerts_id", "alerts", ["id"])
    op.create_index("ix_alerts_company_id", "alerts", ["company_id"])
    op.create_index("ix_alerts_user_id", "alerts", ["user_id"])
    op.create_index("ix_alerts_alert_type", "alerts", ["alert_type"])
    op.create_index("ix_alerts_severity", "alerts", ["severity"])
    op.create_index("ix_alerts_created_at", "alerts", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_alerts_created_at", table_name="alerts")
    op.drop_index("ix_alerts_severity", table_name="alerts")
    op.drop_index("ix_alerts_alert_type", table_name="alerts")
    op.drop_index("ix_alerts_user_id", table_name="alerts")
    op.drop_index("ix_alerts_company_id", table_name="alerts")
    op.drop_index("ix_alerts_id", table_name="alerts")
    op.drop_table("alerts")

    op.drop_index("ix_risk_scores_calculated_at", table_name="risk_scores")
    op.drop_index("ix_risk_scores_risk_level", table_name="risk_scores")
    op.drop_index("ix_risk_scores_company_id", table_name="risk_scores")
    op.drop_index("ix_risk_scores_id", table_name="risk_scores")
    op.drop_table("risk_scores")

    op.drop_index("ix_financials_fiscal_year", table_name="financials")
    op.drop_index("ix_financials_company_id", table_name="financials")
    op.drop_index("ix_financials_id", table_name="financials")
    op.drop_table("financials")

    op.drop_index("ix_companies_state", table_name="companies")
    op.drop_index("ix_companies_country", table_name="companies")
    op.drop_index("ix_companies_sector", table_name="companies")
    op.drop_index("ix_companies_ticker", table_name="companies")
    op.drop_index("ix_companies_name", table_name="companies")
    op.drop_index("ix_companies_id", table_name="companies")
    op.drop_table("companies")

    # Drop enums
    alert_severity_enum.drop(op.get_bind(), checkfirst=True)
    alert_type_enum.drop(op.get_bind(), checkfirst=True)
    risk_level_enum.drop(op.get_bind(), checkfirst=True)
    exchange_enum.drop(op.get_bind(), checkfirst=True)
