"""
OZARK — Alert SQLAlchemy Model

User-facing alerts for companies — risk thresholds, price moves, etc.
"""

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.postgres import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.company import Company
    from app.models.user import User


class AlertType(str, enum.Enum):
    RISK_THRESHOLD = "RISK_THRESHOLD"
    PRICE_MOVEMENT = "PRICE_MOVEMENT"
    EARNINGS = "EARNINGS"
    REGULATORY = "REGULATORY"
    CUSTOM = "CUSTOM"


class AlertSeverity(str, enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Alert(UUIDMixin, Base):
    __tablename__ = "alerts"

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # NULL = system-wide alert, not user-specific
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    alert_type: Mapped[AlertType] = mapped_column(
        Enum(AlertType, name="alert_type_enum"), nullable=False, index=True
    )
    severity: Mapped[AlertSeverity] = mapped_column(
        Enum(AlertSeverity, name="alert_severity_enum"), nullable=False, index=True
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Arbitrary JSON payload (threshold values, old/new scores, etc.)
    # Mapped to 'metadata' column in Postgres while avoiding Base.metadata collision
    alert_metadata: Mapped[Optional[dict]] = mapped_column(
        "metadata", JSONB, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="alerts")
    user: Mapped[Optional["User"]] = relationship("User", back_populates="alerts")

    def __repr__(self) -> str:
        return (
            f"<Alert type={self.alert_type} severity={self.severity} "
            f"company={self.company_id}>"
        )
