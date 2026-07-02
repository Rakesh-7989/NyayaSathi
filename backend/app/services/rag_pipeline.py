import os
import json
from typing import List, Optional
from pathlib import Path
from pydantic import BaseModel


class Citation(BaseModel):
    act: str
    section: str
    text: str


class RAGResult(BaseModel):
    answer: str
    citations: List[Citation]
    language: str = "en"


MOCK_ANSWERS = {
    "arrest": {
        "te": "పోలీసులు వారెంట్ లేకుండా అరెస్ట్ చేయలేరు. BNSS Section 35 ప్రకారం, వారెంట్ లేకుండా అరెస్ట్ చేయాలంటే కొన్ని షరతులు ఉన్నాయి:\n\n1. హత్య, దోపిడీ వంటి తీవ్రమైన నేరాలకు మాత్రమే వారెంట్ లేకుండా అరెస్ట్ చేయవచ్చు\n2. సామాన్య నేరాలకు వారెంట్ తప్పనిసరి\n3. అరెస్ట్ చేసిన 24 గంటలలోపు మెజిస్ట్రేట్ ముందు హాజరుపరచాలి\n4. అరెస్ట్ చేసిన కారణం తెలియజేయడం తప్పనిసరి\n\n📌 మీ హక్కు: 'నేను ఏ నేరం చేశాను? వారెంట్ చూపించండి' అని అడగండి.",
        "en": "The police cannot arrest you without a warrant in most cases. Under BNSS Section 35, arrest without warrant is only allowed for serious offenses.",
        "citations": [
            Citation(act="BNSS 2023", section="Section 35", text="Arrest without warrant - conditions for police arrest"),
            Citation(act="Constitution of India", section="Article 22", text="Protection against arrest and detention"),
            Citation(act="BNSS 2023", section="Section 46", text="Arrest how made"),
        ],
    },
    "rent": {
        "te": "అద్దె పెంచడానికి నిర్దిష్ట నియమాలు ఉన్నాయి:\n\n1. అద్దె ఒప్పందంలో పేర్కొన్న నిబంధనల ప్రకారం మాత్రమే పెంచవచ్చు\n2. సాధారణంగా సంవత్సరానికి 10-15% మించి పెంచకూడదు\n3. అద్దె పెంచాలంటే కనీసం 30 రోజుల ముందుగానే నోటీసు ఇవ్వాలి\n4. రెంట్ కంట్రోల్ చట్టం వర్తించే ప్రాంతాల్లో ప్రభుత్వ నిబంధనలు వర్తిస్తాయి",
        "en": "Landlords can increase rent as per the rental agreement terms. Generally 10-15% annual increase is standard.",
        "citations": [
            Citation(act="Rental Control Act", section="Section 6", text="Landlord's right to increase rent"),
            Citation(act="Transfer of Property Act 1882", section="Section 105", text="Lease defined"),
        ],
    },
    "salary": {
        "te": "కంపెనీ జీతం ఇవ్వకపోతే:\n\n1. ముందుగా HR/మేనేజ్‌మెంట్ కు లిఖిత పూర్వకంగా ఫిర్యాదు చేయండి\n2. లేబర్ డిపార్ట్‌మెంట్ కు ఫిర్యాదు చేయండి (helpline: 19647)\n3. Payment of Wages Act, 1936 ప్రకారం చర్య తీసుకోండి\n4. అవసరమైతే లీగల్ నోటీసు పంపించండి\n\nకంపెనీ జీతం ఆపడం చట్టవిరుద్ధం.",
        "en": "If your company isn't paying salary, file a complaint with the Labour Department.",
        "citations": [
            Citation(act="Payment of Wages Act 1936", section="Section 4", text="Fixation of wage periods"),
            Citation(act="Industrial Disputes Act 1947", section="Section 25F", text="Conditions precedent to retrenchment"),
        ],
    },
    "cheque": {
        "te": "చెక్ బౌన్స్ అయితే:\n\n1. బ్యాంకు నుండి చెక్ బౌన్స్ మెమో తీసుకోండి\n2. చెక్ బౌన్స్ అయిన 30 రోజులలోపు లీగల్ నోటీసు పంపించండి\n3. నోటీసు అందిన 15 రోజులలోపు చెల్లించకపోతే కేసు నమోదు చేయవచ్చు\n4. NI Act Section 138 ప్రకారం 2 సంవత్సరాల జైలు శిక్ష + జరిమానా వరకు విధించవచ్చు",
        "en": "For cheque bounce, send a legal notice within 30 days of bank returning the cheque.",
        "citations": [
            Citation(act="Negotiable Instruments Act 1881", section="Section 138", text="Dishonour of cheque for insufficiency of funds"),
        ],
    },
}

DEFAULT_MOCK = {
    "te": "మీ ప్రశ్నకు సమాధానం తెలుసుకోవడానికి నేను India Code, Supreme Court Judgments, మరియు ఇతర లీగల్ డేటాబేస్ లను సెర్చ్ చేస్తున్నాను.\n\n⚠️ ప్రస్తుతం RAG పైప్‌లైన్ సిద్ధంగా లేదు. దయచేసి OpenAI API key ని .env ఫైల్‌లో కాన్ఫిగర్ చేయండి.\n\nమీరు ఈ విషయాలపై అడగవచ్చు: అరెస్ట్, అద్దె, జీతం, చెక్ బౌన్స్, సైబర్ నేరం, వినియోగదారుల హక్కులు.",
    "en": "I'm searching through Indian legal databases for your answer. Currently the RAG pipeline is in demo mode.",
    "citations": [],
}

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


class RAGPipeline:
    def __init__(self):
        self.initialized = True
        self.knowledge_base = {}

    async def initialize(self):
        pass

    def _find_answer(self, question: str) -> dict:
        question_lower = question.lower()
        for keyword, answer in MOCK_ANSWERS.items():
            if keyword in question_lower:
                return answer
        return DEFAULT_MOCK

    async def query(
        self,
        question: str,
        language: str = "te",
        top_k: int = 5,
    ) -> RAGResult:
        result = self._find_answer(question)
        answer_text = result.get(language, result.get("te", result["en"]))
        citations = result.get("citations", [])

        return RAGResult(
            answer=answer_text,
            citations=citations,
            language=language,
        )

    async def add_document(self, text: str, metadata: dict):
        pass

    async def search_similar(self, query: str, k: int = 5):
        return []


rag_pipeline = RAGPipeline()
