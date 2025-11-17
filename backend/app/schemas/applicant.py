# Ensure Applicant is defined after ApplicantCreate and all imports
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class FinancialData(BaseModel):
    monthly_income: float = Field(..., gt=0)
    monthly_expenses: float = Field(..., ge=0)
    savings: float = Field(..., ge=0)
    existing_loans: float = Field(default=0, ge=0)
    payment_history_score: float = Field(default=0, ge=0, le=100)

class SocialData(BaseModel):
    social_connections: int = Field(default=0, ge=0)
    community_engagement_score: float = Field(default=0, ge=0, le=100)
    references_count: int = Field(default=0, ge=0)
    online_reputation_score: float = Field(default=0, ge=0, le=100)

class GigData(BaseModel):
    platforms: list[str] = Field(default_factory=list)
    total_gigs_completed: int = Field(default=0, ge=0)
    average_rating: float = Field(default=0, ge=0, le=5)
    active_months: int = Field(default=0, ge=0)
    income_consistency_score: float = Field(default=0, ge=0, le=100)

class ApplicantCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    financial_data: Optional[FinancialData] = None
    social_data: Optional[SocialData] = None
    gig_data: Optional[GigData] = None

# The correct Applicant class
class Applicant(ApplicantCreate):
    id: Optional[str] = None
    user_id: Optional[str] = None
    credit_score: Optional[float] = None
    risk_tier: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# ...existing code for ApplicantResponse, IngestFinancialRequest, etc...

# ...existing code...

# Place Applicant after ApplicantCreate

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class FinancialData(BaseModel):
    monthly_income: float = Field(..., gt=0)
    monthly_expenses: float = Field(..., ge=0)
    savings: float = Field(..., ge=0)
    existing_loans: float = Field(default=0, ge=0)
    payment_history_score: float = Field(default=0, ge=0, le=100)


class SocialData(BaseModel):
    social_connections: int = Field(default=0, ge=0)
    community_engagement_score: float = Field(default=0, ge=0, le=100)
    references_count: int = Field(default=0, ge=0)
    online_reputation_score: float = Field(default=0, ge=0, le=100)


class GigData(BaseModel):
    platforms: list[str] = Field(default_factory=list)
    total_gigs_completed: int = Field(default=0, ge=0)
    average_rating: float = Field(default=0, ge=0, le=5)
    active_months: int = Field(default=0, ge=0)
    income_consistency_score: float = Field(default=0, ge=0, le=100)


class ApplicantCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    financial_data: Optional[FinancialData] = None
    social_data: Optional[SocialData] = None
    gig_data: Optional[GigData] = None


class ApplicantResponse(BaseModel):
    id: str
    user_id: str
    name: str
    email: str
    phone: Optional[str] = None
    financial_data: Optional[FinancialData] = None
    social_data: Optional[SocialData] = None
    gig_data: Optional[GigData] = None
    credit_score: Optional[float] = None
    risk_tier: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class IngestFinancialRequest(BaseModel):
    applicant_id: str
    data: FinancialData


class IngestSocialRequest(BaseModel):
    applicant_id: str
    data: SocialData


class IngestGigRequest(BaseModel):
    applicant_id: str
    data: GigData
