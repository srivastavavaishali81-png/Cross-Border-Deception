"""
OZARK — Alert Schemas (Pydantic v2)
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.models.alert import AlertSeverity, AlertType


class AlertBase(BaseModel):
    company_id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    alert_type: AlertType
    severity: AlertSeverity
    title: str = Field(..., max_length=255)
    message: str
    metadata: Optional[Dict[str, Any]] = None


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    is_read: Optional[bool] = None
    is_resolved: Optional[bool] = None
    title: Optional[str] = None
    message: Optional[str] = None


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    company_id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    message: str
    is_read: bool
    is_resolved: bool
    resolved_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = Field(default=None, validation_alias="alert_metadata")
    created_at: datetime
