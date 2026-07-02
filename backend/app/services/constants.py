from pathlib import Path
from pydantic import BaseModel
from typing import List


class Citation(BaseModel):
    act: str
    section: str
    text: str


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FAQ_PATH = DATA_DIR / "legal_faq.json"
CHROMA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "chroma_db"
