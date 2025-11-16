from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings
from typing import Optional


class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None


mongodb = MongoDB()


async def connect_to_mongo():
    """Connect to MongoDB"""
    mongodb.client = AsyncIOMotorClient(settings.mongodb_uri)
    mongodb.db = mongodb.client[settings.mongodb_db]
    
    # Ensure indexes
    await ensure_indexes()
    print(f"Connected to MongoDB: {settings.mongodb_db}")


async def close_mongo_connection():
    """Close MongoDB connection"""
    if mongodb.client:
        mongodb.client.close()
        print("Closed MongoDB connection")


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    if mongodb.db is None:
        raise Exception("Database not initialized")
    return mongodb.db


async def ensure_indexes():
    """Create necessary database indexes"""
    db = mongodb.db
    
    # Users collection indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index("google_id", unique=True, sparse=True)
    
    # Applicants collection indexes
    await db.applicants.create_index("user_id")
    await db.applicants.create_index("created_at")
    
    # Predictions collection indexes
    await db.predictions.create_index("user_id")
    await db.predictions.create_index("applicant_id")
    await db.predictions.create_index("created_at")
    
    print("Database indexes ensured")
