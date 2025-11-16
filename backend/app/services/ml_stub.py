"""
ML Service - CatBoost Model Implementation

This service loads and uses the trained CatBoost model for credit scoring.
"""

import os
from pathlib import Path
from typing import Dict, Any, List
from catboost import CatBoostRegressor
import numpy as np


# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
MODEL_PATH = os.path.join(BASE_DIR, "models", "catboost_model_best.cbm")

# Load the model at module initialization (singleton pattern)
try:
    model = CatBoostRegressor()
    model.load_model(MODEL_PATH)
    print(f"✓ CatBoost model loaded successfully from {MODEL_PATH}")
    print(f"  Model features: {model.feature_names_}")
except Exception as e:
    print(f"✗ Error loading CatBoost model: {e}")
    model = None


def normalize_features(data: Dict[str, Any]) -> np.ndarray:
    """
    Extract and normalize features from applicant data
    
    Args:
        data: Applicant data with financial_data, social_data, gig_data
        
    Returns:
        Numpy array of features ready for model prediction
    """
    financial = data.get("financial_data", {}) or {}
    social = data.get("social_data", {}) or {}
    gig = data.get("gig_data", {}) or {}
    
    # Extract raw features with defaults
    monthly_income = float(financial.get("monthly_income", 30000))
    monthly_expenses = float(financial.get("monthly_expenses", 20000))
    savings = float(financial.get("savings", 10000))
    
    # Avoid division by zero
    income = max(monthly_income, 1)
    
    # Calculate derived features matching your model training
    # Adjust based on what features your model was trained with
    features = [
        monthly_income / 100000,  # Normalize income
        monthly_expenses / 100000,  # Normalize expenses
        savings / 50000,  # Normalize savings
    ]
    
    return np.array(features).reshape(1, -1)


def classify_risk_tier(score: int) -> str:
    """Classify risk tier based on credit score"""
    if score >= 750:
        return "low"
    elif score >= 650:
        return "medium"
    elif score >= 550:
        return "high"
    else:
        return "very_high"


def predict_credit_score(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict credit score using the trained CatBoost model
    
    Args:
        data: Applicant data including financial, social, and gig signals
        
    Returns:
        Dictionary with score, risk_tier, feature_importances, and confidence
    """
    
    if model is None:
        raise Exception("CatBoost model not loaded. Please check model file path.")
    
    # Get feature vector
    feature_vector = normalize_features(data)
    
    # Get prediction
    raw_score = model.predict(feature_vector)[0]
    
    # Ensure score is in valid range (300-850 for FICO scale)
    score = int(np.clip(raw_score, 300, 850))
    
    # Determine risk tier
    risk_tier = classify_risk_tier(score)
    
    # Get feature importances from the model
    try:
        feature_importances_values = model.get_feature_importance()
    except:
        # If feature importance fails, create uniform distribution
        feature_importances_values = [33.33, 33.33, 33.34]
    
    # Feature names for display (match the model's 3 features)
    feature_names = ["Normalized Income", "Normalized Expenses", "Normalized Savings"]
    
    # Get actual feature values from input
    financial = data.get("financial_data", {}) or {}
    feature_values = [
        float(financial.get("monthly_income", 30000)),
        float(financial.get("monthly_expenses", 20000)),
        float(financial.get("savings", 10000))
    ]
    
    # Create feature importance list
    feature_importances = []
    for fname, importance, value in zip(feature_names, feature_importances_values, feature_values):
        feature_importances.append({
            "feature": fname,
            "importance": float(importance / 100),  # Normalize to 0-1 range
            "value": float(value)
        })
    
    # Sort by importance (descending)
    feature_importances.sort(key=lambda x: x["importance"], reverse=True)
    
    # Calculate confidence
    confidence = 0.85  # Default confidence
    
    return {
        "score": score,
        "risk_tier": risk_tier,
        "feature_importances": feature_importances,
        "confidence": round(confidence, 2)
    }
