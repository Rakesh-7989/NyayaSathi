import os
import json
import logging
from typing import List

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from app.services.constants import FAQ_PATH, CHROMA_DIR

logger = logging.getLogger(__name__)

COLLECTION_NAME = "legal_faq"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

_model = None
_client = None
_collection = None
_ready = False


def _initialize():
    global _model, _client, _collection, _ready
    try:
        os.makedirs(CHROMA_DIR, exist_ok=True)

        _model = SentenceTransformer(EMBEDDING_MODEL)
        logger.info("Loaded embedding model: %s", EMBEDDING_MODEL)

        _client = chromadb.PersistentClient(
            path=str(CHROMA_DIR),
            settings=Settings(anonymized_telemetry=False),
        )

        existing_collections = [c.name for c in _client.list_collections()]

        if COLLECTION_NAME in existing_collections:
            _collection = _client.get_collection(COLLECTION_NAME)
            logger.info("ChromaDB collection exists (docs: %d)", _collection.count())
        else:
            _collection = _client.create_collection(COLLECTION_NAME)
            _index_faq()
            logger.info("Created and indexed ChromaDB (%d docs)", _collection.count())

        _ready = True
        logger.info("Embedding service ready")
    except Exception as e:
        logger.warning("Embedding service init failed: %s. Falling back to keyword matching.", e)
        _ready = False


def _index_faq():
    if not FAQ_PATH.exists():
        logger.warning("FAQ file not found, skipping index")
        return

    with open(FAQ_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    ids = []
    documents = []
    metadatas = []

    for i, entry in enumerate(data):
        text = " ".join([
            entry.get("question_te", ""),
            entry.get("question_en", ""),
            " ".join(entry.get("keywords", [])),
        ])
        ids.append(str(i))
        documents.append(text)
        metadatas.append({
            "id": entry.get("id", str(i)),
            "topics": ",".join(entry.get("topics", [])),
        })

    batch_size = 100
    for start in range(0, len(ids), batch_size):
        end = start + batch_size
        _collection.add(
            ids=ids[start:end],
            documents=documents[start:end],
            metadatas=metadatas[start:end],
        )


def search(query: str, k: int = 5) -> List[dict]:
    global _collection, _ready
    if not _ready or _collection is None:
        return []
    try:
        count = _collection.count()
        if count == 0:
            return []
        results = _collection.query(
            query_texts=[query],
            n_results=min(k, count),
        )
        entries = []
        if results and results.get("ids") and results["ids"][0]:
            with open(FAQ_PATH, "r", encoding="utf-8") as f:
                faq_data = json.load(f)
            for i, doc_id in enumerate(results["ids"][0]):
                idx = int(doc_id)
                if 0 <= idx < len(faq_data):
                    entry = dict(faq_data[idx])
                    distance = results["distances"][0][i] if results.get("distances") else 0
                    entry["_score"] = 1.0 - min(distance, 1.0)
                    entries.append(entry)
        return sorted(entries, key=lambda x: x.get("_score", 0), reverse=True)
    except Exception as e:
        logger.warning("ChromaDB search failed: %s", e)
        return []


_initialize()
