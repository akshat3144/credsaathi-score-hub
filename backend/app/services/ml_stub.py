"""
ML Service - Stub Implementation

This is a placeholder for the actual ML model.
Replace this with your trained credit scoring model.

To integrate your model:
1. Load your trained model (pickle, joblib, or ONNX)
2. Implement feature engineering matching your training pipeline
3. Return predictions in the same format
"""

import random
from typing import Dict, Any, List


def normalize_features(data: Dict[str, Any]) -> Dict[str, float]:
    """
    Normalize input features for ML model
    
    In production, this should match your training normalization
    """
    financial = data.get("financial_data", {})
    social = data.get("social_data", {})
    gig = data.get("gig_data", {})
    
    # Example feature extraction
    features = {
        "income": financial.get("monthly_income", 0),
        "expense_ratio": (
            financial.get("monthly_expenses", 0) / max(financial.get("monthly_income", 1), 1)
        ),
        "savings_ratio": (
            financial.get("savings", 0) / max(financial.get("monthly_income", 1) * 3, 1)
        ),
        "loan_burden": financial.get("existing_loans", 0),
        "payment_history": financial.get("payment_history_score", 0),
        "social_score": social.get("community_engagement_score", 0),
        "gig_rating": gig.get("average_rating", 0),
        "gig_consistency": gig.get("income_consistency_score", 0),
        "gig_experience": gig.get("total_gigs_completed", 0),
    }
    
    return features


def predict_credit_score(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict credit score from applicant data
    
    Args:
        data: Applicant data including financial, social, and gig signals
        
    Returns:
        Dictionary with score, risk_tier, and feature_importances
        
    TODO: Replace with actual model inference
    - Load trained model (e.g., from models/credit_model.pkl)
    - Use model.predict(features) for actual scoring
    - Return real feature importances from your model
    """
    
    # Extract and normalize features
    features = normalize_features(data)
    
    # STUB: Generate mock prediction
    # In production, replace with: score = loaded_model.predict(features)
    
    # Simple heuristic for demonstration
    score = 300  # Base score
    
    # Add points based on features
    if features["income"] > 0:
        score += min(features["income"] / 100, 200)
    
    if features["expense_ratio"] < 0.7:
        score += 50
    
    score += features["payment_history"] * 2
    score += features["social_score"] * 0.5
    score += features["gig_rating"] * 30
    score += features["gig_consistency"] * 1.5
    
    # Cap score between 300-850 (FICO scale)
    score = max(300, min(850, int(score)))
    
    # Determine risk tier
    if score >= 750:
        risk_tier = "low"
    elif score >= 650:
        risk_tier = "medium"
    elif score >= 550:
        risk_tier = "high"
    else:
        risk_tier = "very_high"
    
    # Mock feature importances (replace with actual SHAP values or model importances)
    feature_importances = [
        {"feature": "Monthly Income", "importance": 0.25, "value": features["income"]},
        {"feature": "Payment History", "importance": 0.20, "value": features["payment_history"]},
        {"feature": "Expense Ratio", "importance": 0.15, "value": features["expense_ratio"]},
        {"feature": "Gig Consistency", "importance": 0.15, "value": features["gig_consistency"]},
        {"feature": "Gig Rating", "importance": 0.12, "value": features["gig_rating"]},
        {"feature": "Social Score", "importance": 0.08, "value": features["social_score"]},
        {"feature": "Savings Ratio", "importance": 0.05, "value": features["savings_ratio"]},
    ]
    
    return {
        "score": score,
        "risk_tier": risk_tier,
        "feature_importances": feature_importances,
        "confidence": round(random.uniform(0.75, 0.95), 2)  # Mock confidence
    }


# Example: How to load a real model
"""
import joblib
import numpy as np

# Load at module level (once)
MODEL_PATH = "models/credit_model.pkl"
model = joblib.load(MODEL_PATH)

def predict_credit_score(data: Dict[str, Any]) -> Dict[str, Any]:
    features = normalize_features(data)
    feature_vector = np.array(list(features.values())).reshape(1, -1)
    
    score = int(model.predict(feature_vector)[0])
    probabilities = model.predict_proba(feature_vector)[0]
    
    # Get feature importances from tree-based model
    importances = model.feature_importances_
    feature_importances = [
        {"feature": name, "importance": float(imp), "value": val}
        for name, imp, val in zip(features.keys(), importances, features.values())
    ]
    
    return {
        "score": score,
        "risk_tier": classify_risk(score),
        "feature_importances": sorted(feature_importances, key=lambda x: x["importance"], reverse=True),
        "confidence": float(max(probabilities))
    }
"""
