from fastapi import APIRouter
from pydantic import BaseModel
from app.services.legal_agent import legal_agent

router = APIRouter()


class HealthCheckRequest(BaseModel):
    responses: dict


class HealthCheckResponse(BaseModel):
    score: int
    recommendations: list[str]


QUESTIONS = [
    {"key": "has_pan", "question_te": "మీ వద్ద PAN కార్డు ఉందా?", "question_en": "Do you have a PAN card?"},
    {"key": "aadhaar_linked", "question_te": "ఆధార్ లింక్ చేశారా?", "question_en": "Is Aadhaar linked?"},
    {"key": "pf_active", "question_te": "PF ఖాతా యాక్టివ్‌గా ఉందా?", "question_en": "Is PF account active?"},
    {"key": "has_insurance", "question_te": "ఇన్సూరెన్స్ ఉందా?", "question_en": "Do you have insurance?"},
    {"key": "has_will", "question_te": "విల్ రాశారా?", "question_en": "Have you created a will?"},
    {"key": "rental_agreement", "question_te": "అద్దె ఒప్పందం ఉందా?", "question_en": "Do you have a rental agreement?"},
    {"key": "marriage_registered", "question_te": "పెళ్లి రిజిస్ట్రేషన్ చేశారా?", "question_en": "Is marriage registered?"},
    {"key": "has_gst", "question_te": "GST రిజిస్ట్రేషన్ ఉందా?", "question_en": "Do you have GST registration?"},
    {"key": "company_registered", "question_te": "కంపెనీ రిజిస్ట్రేషన్ చేశారా?", "question_en": "Is your company registered?"},
]


@router.get("/questions")
def get_questions(language: str = "te"):
    return {"questions": QUESTIONS}


@router.post("/assess", response_model=HealthCheckResponse)
async def assess_health(request: HealthCheckRequest):
    result = await legal_agent.legal_health_check(request.responses)
    return HealthCheckResponse(
        score=result["score"],
        recommendations=result["recommendations"],
    )
