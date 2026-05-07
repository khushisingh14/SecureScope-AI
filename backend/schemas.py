from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class FindingBase(BaseModel):
    title: str
    severity: str
    description: str
    affected_host: str
    remediation: str = ""
    references: str = ""
    source: str


class FindingRead(FindingBase):
    id: int
    ai_analysis: str = ""
    priority: int
    created_at: datetime
    scan_id: int

    class Config:
        from_attributes = True


class ScanRead(BaseModel):
    id: int
    name: str
    scanner_type: str
    filename: str
    scope: str
    risk_score: float
    created_at: datetime
    findings: list[FindingRead] = []

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    scan_count: int
    finding_count: int
    posture_score: float
    severity_counts: dict[str, int]
    source_counts: dict[str, int]
    recent_scans: list[ScanRead]


class AIRequest(BaseModel):
    finding_id: int | None = None
    prompt: str | None = None
