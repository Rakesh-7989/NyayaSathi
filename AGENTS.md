# NyayaSathi — Session Context

## Overview
AI Legal Assistant (NyayaSathi = న్యాయసాథి) for Indian citizens with Telugu-first legal Q&A, document analysis, health check, and complaint generation. FastAPI backend + Next.js 16 frontend.

## Constraints (CRITICAL)
- **Zero cost** — no paid APIs/services
- **No Docker** — SQLite, in-process vector DB
- **No API keys** — mock mode until keys are added
- Python 3.10, Windows, PowerShell 5.1

## What's Done

### Backend (`backend/`)
- FastAPI app at `backend/app/main.py`, port 8000
- 4 routers: `chat`, `documents`, `health_check`, `complaints` under `/api/v1/`
- SQLite at `backend/nyayasathi.db` (`check_same_thread=False`)
- Alembic, CORS enabled for `http://localhost:3000`

### Phase 1 — Comprehensive Legal FAQ ✅
- `backend/app/data/legal_faq.json` — 64 Q&A entries across 14 domains
- Domains: Constitution (5), BNS (8), BNSS (7), BSA (3), Consumer (5), RTI (3), Labour (5), Motor Vehicles (4), Property (4), Family (6), Cyber (4), NI Act (2), Business (2), General (4)
- Each entry: Telugu + English answers, citations (act/section/text)
- Loaded at runtime, not hardcoded
- Scored keyword fallback matching (threshold ≥ 4)

### Phase 2 — ChromaDB + Vector Search ✅
- `backend/app/services/embeddings.py` — ChromaDB PersistentClient + sentence-transformers `all-MiniLM-L6-v2`
- Storage at `backend/data/chroma_db/` (gitignored)
- RAG pipeline (`backend/app/services/rag_pipeline.py`): vector search primary, keyword fallback secondary
- `backend/app/services/constants.py` — shared constants (Citation, FAQ_PATH, CHROMA_DIR)
- Removed Qdrant/OpenAI/LangChain deps from `requirements.txt`

### Phase 3-6 — NOT STARTED

### Frontend (`frontend/`)
- Next.js 16 + Tailwind v4 + ShadCN UI
- Pages: Landing (`/`), Chat (`/chat`), Health Check (`/health-check`), Documents (`/documents`), Complaints (`/complaints`)
- Each page has graceful mock fallback if backend is unreachable

## Architecture

### Data Flow
```
User Query → FastAPI Router → LegalAgent → RAGPipeline.query()
                                              ├── EmbeddingService.search() [ChromaDB vector]
                                              └── _keyword_fallback() [scored keyword match]
                                    → RAGResult(answer, citations)
```

### Key Files
| File | Purpose |
|------|---------|
| `backend/app/services/rag_pipeline.py` | RAG orchestration, vector + keyword matching |
| `backend/app/services/embeddings.py` | ChromaDB + sentence-transformers setup |
| `backend/app/services/legal_agent.py` | Complaint templates, document analysis, health check |
| `backend/app/services/constants.py` | Shared models (Citation), paths |
| `backend/app/data/legal_faq.json` | 64 legal Q&A entries |
| `backend/app/routers/` | FastAPI route handlers (4 files) |
| `backend/app/models/` | SQLAlchemy models (User, ChatSession, Message, Document, HealthCheck) |
| `backend/app/db/session.py` | SQLite engine + session |
| `backend/app/main.py` | FastAPI app, CORS, startup |

### Running
```powershell
# Backend
cd backend; .\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend; npm run dev
```

### Testing
```powershell
curl -X POST "http://localhost:8000/api/v1/chat" -H "Content-Type: application/json" -d '{"message":"arrest rights","language":"en"}'
```

## Known Issues
- Telugu chars display garbled in PowerShell terminal (UTF-8 data is correct, terminal encoding issue)
- `backend/venv/` not in `.gitignore` — should be added
- Complaint templates have hardcoded placeholders (`{name}`, `{address}`)
- No authentication (all sessions are "new")

## Planned (Phase Order)
1. ✅ Expand mock Q&A (64 FAQ entries)
2. ✅ ChromaDB + local embeddings (sentence-transformers)
3. ❏ Real document analysis (10+ document types with clause detection)
4. ❏ Ollama local LLM integration
5. ❏ Frontend polish (loading states, error boundaries, mobile)
6. ❏ Auth (NextAuth + GitHub OAuth)

## Environment
```powershell
py -3.10          # Python launcher (WindowsApps alias broken)
.\venv\Scripts\python.exe  # venv Python
```
