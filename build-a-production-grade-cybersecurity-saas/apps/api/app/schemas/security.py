from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserRead(BaseModel):
    id: str
    email: EmailStr
    role: Literal["admin", "analyst", "viewer"]


class DomainScanRequest(BaseModel):
    domain: str = Field(pattern=r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


class Finding(BaseModel):
    category: str
    key: str
    status: Literal["pass", "warn", "fail"]
    severity: Literal["critical", "high", "medium", "low", "info"]
    message: str
    evidence: dict = Field(default_factory=dict)


class Recommendation(BaseModel):
    title: str
    priority: Literal["critical", "high", "medium", "low"]
    remediation: str
    finding_key: str


class ScanResponse(BaseModel):
    domain: str
    risk_score: float
    findings: list[Finding]
    recommendations: list[Recommendation]
    scanned_at: datetime


class DashboardResponse(BaseModel):
    risk_score: float
    trend: list[dict]
    active_alerts: list[dict]
    recommendations: list[Recommendation]


class RiskSimulationRequest(BaseModel):
    current_score: float | None = Field(default=None, ge=0, le=100)
    findings: list[Finding]
    selected_finding_keys: list[str] = Field(default_factory=list)


class RiskSimulationFixImpact(BaseModel):
    finding_key: str
    title: str
    category: str
    severity: Literal["critical", "high", "medium", "low", "info"]
    score_impact: float
    risk_reduction: float


class RiskSimulationResponse(BaseModel):
    current_score: float
    predicted_score: float
    improvement: float
    improvement_percentage: float
    estimated_risk_reduction: float
    selected_finding_keys: list[str]
    top_fixes: list[RiskSimulationFixImpact]
    comparison: list[dict]
