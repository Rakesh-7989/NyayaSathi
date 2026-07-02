from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, documents, health_check, complaints
from app.db.session import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NyayaSathi API",
    description="AI Legal Companion for Every Indian Citizen",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(health_check.router, prefix="/api/v1/health-check", tags=["Health Check"])
app.include_router(complaints.router, prefix="/api/v1/complaints", tags=["Complaints"])

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}
