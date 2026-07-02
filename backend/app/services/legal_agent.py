from typing import Optional
from app.services.rag_pipeline import rag_pipeline


class LegalAgent:
    def __init__(self):
        self.llm = None

    async def answer_legal_query(
        self,
        question: str,
        language: str = "en",
        user_context: Optional[dict] = None,
    ):
        result = await rag_pipeline.query(question, language=language)
        return result

    async def generate_complaint(
        self,
        complaint_type: str,
        details: dict,
        language: str = "en",
    ):
        template = COMPLAINT_TEMPLATES.get(complaint_type, "")
        return template

    async def analyze_document(self, text: str):
        return {
            "summary": "Document analysis not yet implemented.",
            "risks": [],
            "missing_clauses": [],
            "suggestions": [],
        }

    async def legal_health_check(self, responses: dict) -> dict:
        score = 0
        max_score = len(responses) * 10
        recommendations = []

        for key, value in responses.items():
            if value is True:
                score += 10

        if max_score > 0:
            percentage = round((score / max_score) * 100)
        else:
            percentage = 0

        return {
            "score": percentage,
            "recommendations": recommendations,
        }


legal_agent = LegalAgent()

COMPLAINT_TEMPLATES = {
    "consumer": "Consumer Complaint Template",
    "police": "Police Complaint Template",
    "legal_notice": "Legal Notice Template",
    "rti": "RTI Application Template",
    "cyber_crime": "Cyber Crime Complaint Template",
    "labour": "Labour Complaint Template",
}
