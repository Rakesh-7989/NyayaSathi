from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.legal_agent import legal_agent

router = APIRouter()


class ComplaintRequest(BaseModel):
    complaint_type: str
    details: dict
    language: str = "te"


@router.post("/generate")
async def generate_complaint(request: ComplaintRequest):
    try:
        result = await legal_agent.generate_complaint(
            complaint_type=request.complaint_type,
            details=request.details,
            language=request.language,
        )
        return {"complaint": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
