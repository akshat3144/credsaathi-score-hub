from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.dependencies import get_current_user
from app.services.ml_stub import predict_credit_score
from app.db import get_database
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime
from bson import ObjectId


router = APIRouter(prefix="/predict", tags=["prediction"])


class PredictRequest(BaseModel):
    applicant_id: str


class FeatureImportance(BaseModel):
    feature: str
    importance: float
    value: float


class PredictResponse(BaseModel):
    prediction_id: str
    applicant_id: str
    score: int
    risk_tier: str
    feature_importances: List[FeatureImportance]
    confidence: float
    created_at: datetime


@router.post("/score", response_model=PredictResponse)
async def predict_score(
    request: PredictRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Predict credit score for an applicant
    
    Takes applicant data (financial, social, gig signals),
    runs ML model inference, and returns:
    - Credit score (300-850)
    - Risk tier (low/medium/high/very_high)
    - Feature importances (which signals contributed most)
    - Confidence score
    
    Stores prediction in database for audit trail.
    """
    db = get_database()
    
    # Fetch applicant data (convert string ID to ObjectId)
    try:
        applicant = await db.applicants.find_one({
            "_id": ObjectId(request.applicant_id),
            "user_id": str(current_user["_id"])
        })
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid applicant ID format: {str(e)}"
        )
    
    if not applicant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Applicant not found or access denied"
        )
    
    # Prepare data for ML model
    model_input = {
        "financial_data": applicant.get("financial_data", {}),
        "social_data": applicant.get("social_data", {}),
        "gig_data": applicant.get("gig_data", {})
    }
    
    # Run prediction
    prediction_result = predict_credit_score(model_input)
    
    # Store prediction in database
    prediction_doc = {
        "user_id": str(current_user["_id"]),
        "applicant_id": request.applicant_id,
        "input_data": model_input,
        "score": prediction_result["score"],
        "risk_tier": prediction_result["risk_tier"],
        "feature_importances": prediction_result["feature_importances"],
        "confidence": prediction_result["confidence"],
        "created_at": datetime.utcnow()
    }
    
    result = await db.predictions.insert_one(prediction_doc)
    prediction_id = str(result.inserted_id)
    
    # Update applicant with latest score (use ObjectId)
    await db.applicants.update_one(
        {"_id": ObjectId(request.applicant_id)},
        {
            "$set": {
                "credit_score": prediction_result["score"],
                "risk_tier": prediction_result["risk_tier"],
                "last_scored_at": datetime.utcnow()
            }
        }
    )
    
    return PredictResponse(
        prediction_id=prediction_id,
        applicant_id=request.applicant_id,
        score=prediction_result["score"],
        risk_tier=prediction_result["risk_tier"],
        feature_importances=[
            FeatureImportance(**fi) for fi in prediction_result["feature_importances"]
        ],
        confidence=prediction_result["confidence"],
        created_at=prediction_doc["created_at"]
    )


@router.get("/history/{applicant_id}")
async def get_prediction_history(
    applicant_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get prediction history for an applicant"""
    db = get_database()
    
    predictions = await db.predictions.find({
        "applicant_id": applicant_id,
        "user_id": str(current_user["_id"])
    }).sort("created_at", -1).limit(10).to_list(10)
    
    return {"predictions": predictions}
