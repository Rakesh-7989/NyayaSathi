from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.legal_agent import legal_agent

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = content.decode("utf-8", errors="ignore")
        analysis = await legal_agent.analyze_document(text)
        return {
            "filename": file.filename,
            "analysis": analysis,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
