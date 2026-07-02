import json
import logging
from typing import List, Optional

from pydantic import BaseModel
from app.services.constants import Citation, FAQ_PATH
from app.services import embeddings as embedding_service

logger = logging.getLogger(__name__)


class RAGResult(BaseModel):
    answer: str
    citations: List[Citation]
    language: str = "en"


class FAQEntry(BaseModel):
    id: str
    keywords: List[str]
    topics: List[str]
    question_te: str
    question_en: str
    answer_te: str
    answer_en: str
    citations: List[Citation]

DEFAULT_ANSWER_TE = (
    "\u0c2e\u0c40 \u0c2a\u0c4d\u0c30\u0c36\u0c4d\u0c28\u0c15\u0c41 \u0c38\u0c02\u0c2c\u0c02\u0c27\u0c3f\u0c02\u0c1a\u0c3f\u0c28 \u0c38\u0c2e\u0c3e\u0c1a\u0c3e\u0c30\u0c02 \u0c2a\u0c4d\u0c30\u0c38\u0c4d\u0c24\u0c41\u0c24\u0c02 \u0c2e\u0c3e \u0c21\u0c47\u0c1f\u0c3e\u0c2c\u0c47\u0c38\u0c4d\u200c\u0c32\u0c4b \u0c05\u0c02\u0c26\u0c41\u0c2c\u0c3e\u0c1f\u0c41\u0c32\u0c4b \u0c32\u0c47\u0c26\u0c41.\n\n"
    "\u0c26\u0c2f\u0c1a\u0c47\u0c38\u0c3f \u0c08 \u0c35\u0c3f\u0c37\u0c2f\u0c3e\u0c32\u0c2a\u0c48 \u0c05\u0c21\u0c17\u0c02\u0c21\u0c3f: \u0c05\u0c30\u0c46\u0c38\u0c4d\u0c1f\u0c4d, FIR, \u0c1c\u0c3e\u0c2e\u0c40\u0c28\u0c41, "
    "\u0c26\u0c4a\u0c02\u0c17\u0c24\u0c28\u0c02, \u0c26\u0c3e\u0c21\u0c3f, \u0c39\u0c24\u0c4d\u0c2f, \u0c2e\u0c3e\u0c28\u0c28\u0c37\u0c4d\u0c1f\u0c02, "
    "\u0c2e\u0c4b\u0c38\u0c02, \u0c26\u0c4b\u0c2a\u0c3f\u0c21\u0c40, \u0c15\u0c3f\u0c21\u0c4d\u0c28\u0c3e\u0c2a\u0c4d, \u0c35\u0c3f\u0c28\u0c3f\u0c2f\u0c4b\u0c17\u0c26\u0c3e\u0c30\u0c41\u0c32 \u0c39\u0c15\u0c4d\u0c15\u0c41\u0c32\u0c41, RTI, "
    "\u0c1c\u0c40\u0c24\u0c02, PF, ESI, \u0c30\u0c4b\u0c21\u0c4d\u0c21\u0c41 \u0c2a\u0c4d\u0c30\u0c2e\u0c3e\u0c26\u0c3e\u0c32\u0c41, "
    "\u0c06\u0c38\u0c4d\u0c24\u0c3f \u0c28\u0c2e\u0c4b\u0c26\u0c41, \u0c35\u0c3f\u0c35\u0c3e\u0c39\u0c02, \u0c35\u0c3f\u0c21\u0c3e\u0c15\u0c41\u0c32\u0c41, "
    "\u0c2e\u0c46\u0c2f\u0c3f\u0c02\u0c1f\u0c46\u0c28\u0c46\u0c28\u0c4d\u0c38\u0c4d, \u0c38\u0c48\u0c2c\u0c30\u0c4d \u0c28\u0c47\u0c30\u0c02, \u0c1a\u0c46\u0c15\u0c4d \u0c2c\u0c4c\u0c28\u0c4d\u0c38\u0c4d.\n\n"
    "\u0c32\u0c47\u0c26\u0c3e \u0c2e\u0c40\u0c30\u0c41 \u0c28\u0c4d\u0c2f\u0c3e\u0c2f\u0c35\u0c3e\u0c26\u0c3f\u0c28\u0c3f \u0c38\u0c02\u0c2a\u0c4d\u0c30\u0c26\u0c3f\u0c02\u0c1a\u0c02\u0c21\u0c3f."
)

DEFAULT_ANSWER_EN = (
    "I don\u2019t have information on this topic in my current database. "
    "Please ask about: arrest, FIR, bail, theft, assault, murder, defamation, "
    "cheating, robbery, kidnapping, consumer rights, RTI, salary, PF, ESI, "
    "road accidents, property registration, marriage, divorce, maintenance, "
    "cyber crime, cheque bounce. Or consult a lawyer for specific advice."
)


class RAGPipeline:
    def __init__(self):
        self.initialized = False
        self.faq_entries: List[dict] = []

    async def initialize(self):
        if self.initialized:
            return
        try:
            if FAQ_PATH.exists():
                with open(FAQ_PATH, "r", encoding="utf-8") as f:
                    self.faq_entries = json.load(f)
            self.initialized = True
        except Exception as e:
            logger.error(f"RAG init error: {e}")
            self.initialized = True

    def _load_faq_by_idx(self, idx: int) -> Optional[dict]:
        if 0 <= idx < len(self.faq_entries):
            return self.faq_entries[idx]
        return None

    def _keyword_fallback(self, question: str) -> Optional[dict]:
        question_lower = question.lower()
        best = None
        best_score = 0

        for entry in self.faq_entries:
            score = 0
            for keyword in entry.get("keywords", []):
                if keyword in question_lower:
                    score += len(keyword) * 2
            if score > best_score:
                best_score = score
                best = entry

        if best_score >= 4:
            return best
        return None

    def _entry_to_result(self, entry: dict, language: str) -> RAGResult:
        answer_text = entry.get(f"answer_{language}", entry.get("answer_en", ""))
        citations_raw = entry.get("citations", [])
        citations = [Citation(**c) for c in citations_raw]
        return RAGResult(
            answer=answer_text,
            citations=citations,
            language=language,
        )

    async def query(
        self,
        question: str,
        language: str = "te",
        top_k: int = 5,
    ) -> RAGResult:
        await self.initialize()

        try:
            results = embedding_service.search(question, k=3)
            if results:
                top = results[0]
                score = top.get("_score", 0)
                if score >= 0.3:
                    return self._entry_to_result(top, language)
        except Exception as e:
            logger.debug(f"Vector search failed, using keyword fallback: {e}")

        match = self._keyword_fallback(question)
        if match:
            return self._entry_to_result(match, language)

        return RAGResult(
            answer=DEFAULT_ANSWER_TE if language == "te" else DEFAULT_ANSWER_EN,
            citations=[],
            language=language,
        )

    async def add_document(self, text: str, metadata: dict):
        pass

    async def search_similar(self, query: str, k: int = 5):
        return []


rag_pipeline = RAGPipeline()
