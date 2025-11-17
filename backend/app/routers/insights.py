from fastapi import APIRouter, HTTPException, Depends
import traceback
from ..services.insights_service import get_borrower_insights
from ..schemas.applicant import Applicant
from ..db import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/insights", tags=["insights"])

# Example: POST /insights/generate with applicant data in body
@router.post("/generate")
def generate_insights(applicant: Applicant, db: Session = Depends(get_db)):
    try:
        # Convert applicant Pydantic model to dict
        applicant_data = applicant.dict()
        # Optionally, enrich with more data from DB if needed
        insights = get_borrower_insights(applicant_data)
        return {"insights": insights}
    except Exception as e:
        print("\n--- Exception in /insights/generate ---")
        print(traceback.format_exc())
        print("--- End Exception ---\n")
        raise HTTPException(status_code=500, detail=str(e))