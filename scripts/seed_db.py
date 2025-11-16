"""
Database seeding script

Generates 30 random gig-worker applicant profiles with sample data
for testing the credit scoring system.

Usage:
    python scripts/seed_db.py
"""

import asyncio
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings


FIRST_NAMES = ["Raj", "Priya", "Amit", "Sneha", "Vikram", "Anjali", "Rahul", "Kavya", 
               "Arjun", "Meera", "Sanjay", "Divya", "Kiran", "Pooja", "Arun"]

LAST_NAMES = ["Kumar", "Sharma", "Patel", "Singh", "Reddy", "Nair", "Gupta", "Desai",
              "Iyer", "Mehta", "Joshi", "Rao", "Pillai", "Das", "Menon"]

GIG_PLATFORMS = ["Uber", "Ola", "Swiggy", "Zomato", "Urban Company", "Dunzo", 
                 "Rapido", "Porter", "Amazon Flex", "Freelancer", "Upwork"]


def generate_applicant(index: int) -> dict:
    """Generate a random applicant profile"""
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    email = f"{name.lower().replace(' ', '.')}_{index}@example.com"
    
    # Financial data - varied income levels
    income = random.randint(15000, 80000)
    expense_ratio = random.uniform(0.5, 0.9)
    
    financial_data = {
        "monthly_income": income,
        "monthly_expenses": int(income * expense_ratio),
        "savings": random.randint(5000, 100000),
        "existing_loans": random.randint(0, 200000) if random.random() > 0.4 else 0,
        "payment_history_score": random.randint(40, 100)
    }
    
    # Social data
    social_data = {
        "social_connections": random.randint(50, 500),
        "community_engagement_score": random.randint(30, 95),
        "references_count": random.randint(0, 10),
        "online_reputation_score": random.randint(50, 100)
    }
    
    # Gig data - realistic profiles
    platforms_count = random.randint(1, 4)
    selected_platforms = random.sample(GIG_PLATFORMS, platforms_count)
    
    gig_data = {
        "platforms": selected_platforms,
        "total_gigs_completed": random.randint(10, 2000),
        "average_rating": round(random.uniform(3.5, 5.0), 2),
        "active_months": random.randint(3, 60),
        "income_consistency_score": random.randint(40, 95)
    }
    
    created_at = datetime.utcnow() - timedelta(days=random.randint(1, 365))
    
    return {
        "user_id": "seed_user",  # All seeded applicants belong to a test user
        "name": name,
        "email": email,
        "phone": f"+91{''.join([str(random.randint(0, 9)) for _ in range(10)])}",
        "financial_data": financial_data,
        "social_data": social_data,
        "gig_data": gig_data,
        "credit_score": None,  # Will be calculated when predict endpoint is called
        "risk_tier": None,
        "created_at": created_at,
        "updated_at": created_at
    }


async def seed_database():
    """Seed database with sample data"""
    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.mongodb_db]
    
    print(f"Generating 30 sample applicants...")
    applicants = [generate_applicant(i) for i in range(1, 31)]
    
    # Clear existing seed data
    print("Clearing existing seed data...")
    await db.applicants.delete_many({"user_id": "seed_user"})
    
    # Insert new data
    print("Inserting sample applicants...")
    result = await db.applicants.insert_many(applicants)
    
    print(f"✅ Successfully seeded {len(result.inserted_ids)} applicants!")
    print("\nSample applicants:")
    for i, applicant in enumerate(applicants[:5], 1):
        print(f"  {i}. {applicant['name']} - {applicant['email']}")
        print(f"     Income: ₹{applicant['financial_data']['monthly_income']}/mo")
        print(f"     Platforms: {', '.join(applicant['gig_data']['platforms'])}")
        print(f"     Gigs: {applicant['gig_data']['total_gigs_completed']}, Rating: {applicant['gig_data']['average_rating']}")
    print("  ...")
    
    print("\n⚠️  Note: These applicants are assigned to user_id 'seed_user'")
    print("   You'll need to update user_id after creating a real user via OAuth")
    
    client.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
