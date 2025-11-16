from datetime import datetime, timedelta
from app.db import get_database
from app.utils.security import create_access_token
from app.schemas.user import UserCreate
from typing import Dict, Optional


async def get_or_create_user(google_user_info: Dict) -> Dict:
    """
    Get existing user or create new user from Google OAuth data
    
    Args:
        google_user_info: User info from Google OAuth
        
    Returns:
        User document from database
    """
    db = get_database()
    
    email = google_user_info.get("email")
    google_id = google_user_info.get("sub")
    name = google_user_info.get("name", email)
    picture = google_user_info.get("picture")
    
    # Try to find existing user by google_id or email
    user = await db.users.find_one({
        "$or": [
            {"google_id": google_id},
            {"email": email}
        ]
    })
    
    now = datetime.utcnow()
    
    if user:
        # Update last_login and google_id if needed
        update_data = {"last_login": now}
        if not user.get("google_id"):
            update_data["google_id"] = google_id
        if picture:
            update_data["picture"] = picture
            
        await db.users.update_one(
            {"_id": user["_id"]},
            {"$set": update_data}
        )
        user.update(update_data)
    else:
        # Create new user
        user_data = {
            "email": email,
            "google_id": google_id,
            "name": name,
            "picture": picture,
            "role": "user",
            "created_at": now,
            "last_login": now
        }
        result = await db.users.insert_one(user_data)
        user_data["_id"] = str(result.inserted_id)
        user = user_data
    
    # Ensure _id is string
    user["_id"] = str(user["_id"])
    
    return user


def generate_token_for_user(user: Dict) -> str:
    """
    Generate JWT token for user
    
    Args:
        user: User document from database
        
    Returns:
        JWT access token
    """
    token_data = {"sub": user["_id"]}
    return create_access_token(token_data)
