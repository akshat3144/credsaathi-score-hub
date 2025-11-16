from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.dependencies import get_current_user
from app.schemas.user import UserInDB, UserUpdate
from app.db import get_database
from typing import Dict


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserInDB)
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    """Get current authenticated user's information"""
    return UserInDB(
        id=str(current_user["_id"]),
        email=current_user["email"],
        name=current_user["name"],
        picture=current_user.get("picture"),
        google_id=current_user.get("google_id"),
        role=current_user.get("role", "user"),
        created_at=current_user["created_at"],
        last_login=current_user["last_login"]
    )


@router.patch("/me", response_model=UserInDB)
async def update_current_user(
    user_update: UserUpdate,
    current_user: Dict = Depends(get_current_user)
):
    """Update current user's profile"""
    db = get_database()
    
    update_data = user_update.dict(exclude_unset=True)
    if not update_data:
        return await get_current_user_info(current_user)
    
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$set": update_data}
    )
    
    updated_user = await db.users.find_one({"_id": current_user["_id"]})
    
    return UserInDB(
        id=str(updated_user["_id"]),
        email=updated_user["email"],
        name=updated_user["name"],
        picture=updated_user.get("picture"),
        google_id=updated_user.get("google_id"),
        role=updated_user.get("role", "user"),
        created_at=updated_user["created_at"],
        last_login=updated_user["last_login"]
    )
