"""
Applicant model helpers

MongoDB collection schema documentation
"""

APPLICANT_SCHEMA = {
    "_id": "ObjectId",
    "user_id": "string (references users._id)",
    "name": "string",
    "email": "string",
    "phone": "string (optional)",
    "financial_data": {
        "monthly_income": "float",
        "monthly_expenses": "float",
        "savings": "float",
        "existing_loans": "float",
        "payment_history_score": "float (0-100)"
    },
    "social_data": {
        "social_connections": "int",
        "community_engagement_score": "float (0-100)",
        "references_count": "int",
        "online_reputation_score": "float (0-100)"
    },
    "gig_data": {
        "platforms": "array of strings",
        "total_gigs_completed": "int",
        "average_rating": "float (0-5)",
        "active_months": "int",
        "income_consistency_score": "float (0-100)"
    },
    "credit_score": "int (300-850, optional)",
    "risk_tier": "string (low/medium/high/very_high, optional)",
    "created_at": "datetime",
    "updated_at": "datetime"
}


PREDICTION_SCHEMA = {
    "_id": "ObjectId",
    "user_id": "string",
    "applicant_id": "string",
    "input_data": "object (snapshot of data used)",
    "score": "int (300-850)",
    "risk_tier": "string",
    "feature_importances": "array of objects",
    "confidence": "float (0-1)",
    "created_at": "datetime"
}


# Indexes created in app/db.py
# - user_id
# - created_at
# - applicant_id (for predictions)
