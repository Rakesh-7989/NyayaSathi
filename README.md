# ⚖️ NyayaSathi — AI Legal Companion

**Know Your Rights Before You Need a Lawyer.**

NyayaSathi is an AI-powered Legal Operating System for every Indian citizen. It combines RAG-based legal research, multi-agent AI, document analysis, and complaint generation — all in Telugu, Hindi, and English.

## Features

- 💬 **AI Legal Chat** — Ask legal questions, get answers with act/section citations
- 📄 **Document Analysis** — Upload notices/agreements, AI explains risks & missing clauses
- 🩺 **Legal Health Check** — Score your legal preparedness (PAN, PF, Will, etc.)
- 📝 **Complaint Generator** — Consumer, Police, RTI, Cyber Crime, Labour complaints
- 🎙 **Voice Assistant** — Ask & get answers in Telugu voice
- ⚖️ **Know Your Rights** — One-tap guidance for everyday legal situations

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 + TypeScript + Tailwind CSS + ShadCN |
| Backend | FastAPI + Python 3.12 |
| RAG | LangChain + LlamaIndex + Qdrant |
| LLM | GPT-4o / Gemini (fallback routing) |
| Database | PostgreSQL + SQLAlchemy |
| Voice | Whisper (ASR) + gTTS / ElevenLabs |
| Auth | Clerk |

## Quick Start

### 1. Clone & setup

```bash
git clone https://github.com/Rakesh-7989/NyayaSathi.git
cd NyayaSathi
```

### 2. Backend

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Infrastructure (optional — for RAG)

```bash
docker compose up -d qdrant postgres
```

### 5. Ingest legal data

```bash
cd backend
python -m data.scripts.ingest_acts
python -m data.scripts.build_vector_store
```

## Project Structure

```
NyayaSathi/
├── frontend/          # Next.js app
├── backend/           # FastAPI server
│   ├── app/
│   │   ├── routers/   # API endpoints
│   │   ├── services/  # RAG, legal agent, analysis
│   │   ├── models/    # SQLAlchemy models
│   │   └── db/        # Database session
│   └── data/          # Legal PDFs & scripts
├── scripts/           # Dev/ops scripts
├── docker-compose.yml
└── .env.example
```

## Data Sources (RAG)

- India Code (indiacode.nic.in) — Constitution, BNS, BNSS, BSA, etc.
- eCourtsIndia API — Court case records & judgments
- Indian Kanoon API — 3Cr+ court judgments
- NALSA — Free legal aid info

## License

MIT

---

*Disclaimer: NyayaSathi provides educational legal information only. Not a substitute for professional legal advice.*
