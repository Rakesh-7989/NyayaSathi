from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.legal_agent import legal_agent

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    language: str = "te"


class ChatResponse(BaseModel):
    reply: str
    citations: list[dict] = []
    session_id: str


@router.post("")
async def chat(request: ChatRequest):
    try:
        result = await legal_agent.answer_legal_query(
            question=request.message,
            language=request.language,
        )
        return ChatResponse(
            reply=result.answer,
            citations=[c.model_dump() for c in result.citations],
            session_id=request.session_id or "new",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
