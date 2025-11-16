from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.dependencies import get_current_user
from app.schemas.applicant import (
    ApplicantCreate,
    ApplicantResponse,
    IngestFinancialRequest,
    IngestSocialRequest,
    IngestGigRequest
)
from app.db import get_database
from typing import Dict, List
from datetime import datetime
from bson import ObjectId


router = APIRouter(prefix="/ingest", tags=["data-ingestion"])


@router.post("/applicant", response_model=ApplicantResponse, status_code=status.HTTP_201_CREATED)
async def create_applicant(
    applicant: ApplicantCreate,
    current_user: Dict = Depends(get_current_user)
):
    """Create a new applicant profile"""
    db = get_database()
    
    # Check if applicant with same email already exists for this user
    existing = await db.applicants.find_one({
        "user_id": str(current_user["_id"]),
        "email": applicant.email
    })
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Applicant with this email already exists"
        )
    
    now = datetime.utcnow()
    applicant_doc = {
        "user_id": str(current_user["_id"]),
        "name": applicant.name,
        "email": applicant.email,
        "phone": applicant.phone,
        "financial_data": applicant.financial_data.dict() if applicant.financial_data else None,
        "social_data": applicant.social_data.dict() if applicant.social_data else None,
        "gig_data": applicant.gig_data.dict() if applicant.gig_data else None,
        "credit_score": None,
        "risk_tier": None,
        "created_at": now,
        "updated_at": now
    }
    
    result = await db.applicants.insert_one(applicant_doc)
    applicant_doc["_id"] = str(result.inserted_id)
    
    return ApplicantResponse(
        id=applicant_doc["_id"],
        user_id=applicant_doc["user_id"],
        name=applicant_doc["name"],
        email=applicant_doc["email"],
        phone=applicant_doc.get("phone"),
        financial_data=applicant.financial_data,
        social_data=applicant.social_data,
        gig_data=applicant.gig_data,
        credit_score=None,
        risk_tier=None,
        created_at=applicant_doc["created_at"],
        updated_at=applicant_doc["updated_at"]
    )


@router.get("/applicants", response_model=List[ApplicantResponse])
async def list_applicants(
    current_user: Dict = Depends(get_current_user),
    skip: int = 0,
    limit: int = 50
):
    """List all applicants for current user"""
    db = get_database()
    
    applicants = await db.applicants.find({
        "user_id": str(current_user["_id"])
    }).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    
    return [
        ApplicantResponse(
            id=str(app["_id"]),
            user_id=app["user_id"],
            name=app["name"],
            email=app["email"],
            phone=app.get("phone"),
            financial_data=app.get("financial_data"),
            social_data=app.get("social_data"),
            gig_data=app.get("gig_data"),
            credit_score=app.get("credit_score"),
            risk_tier=app.get("risk_tier"),
            created_at=app["created_at"],
            updated_at=app["updated_at"]
        )
        for app in applicants
    ]


@router.post("/financial")
async def ingest_financial_data(
    request: IngestFinancialRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Update financial data for an applicant"""
    db = get_database()
    
    result = await db.applicants.update_one(
        {
            "_id": request.applicant_id,
            "user_id": str(current_user["_id"])
        },
        {
            "$set": {
                "financial_data": request.data.dict(),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Applicant not found"
        )
    
    return {"status": "success", "message": "Financial data updated"}


@router.post("/social")
async def ingest_social_data(
    request: IngestSocialRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Update social data for an applicant"""
    db = get_database()
    
    result = await db.applicants.update_one(
        {
            "_id": request.applicant_id,
            "user_id": str(current_user["_id"])
        },
        {
            "$set": {
                "social_data": request.data.dict(),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Applicant not found"
        )
    
    return {"status": "success", "message": "Social data updated"}


@router.post("/gig")
async def ingest_gig_data(
    request: IngestGigRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Update gig economy data for an applicant"""
    db = get_database()
    
    result = await db.applicants.update_one(
        {
            "_id": request.applicant_id,
            "user_id": str(current_user["_id"])
        },
        {
            "$set": {
                "gig_data": request.data.dict(),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Applicant not found"
        )
    
    return {"status": "success", "message": "Gig data updated"}
