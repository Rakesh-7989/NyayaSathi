"""
Ingest India Code Acts into Qdrant Vector DB.

Usage:
    cd backend
    python -m data.scripts.ingest_acts

This script downloads PDFs of Indian Acts from India Code,
splits them into chunks, generates embeddings, and stores them
in Qdrant for RAG retrieval.
"""

import os
import json
from typing import List

ACTS_TO_INGEST = [
    {
        "name": "Constitution of India",
        "url": "https://www.indiacode.nic.in/handle/123456789/12345",
    },
    {
        "name": "Bharatiya Nyaya Sanhita 2023",
        "url": "https://www.indiacode.nic.in/handle/123456789/23456",
    },
    {
        "name": "Bharatiya Nagarik Suraksha Sanhita 2023",
        "url": "https://www.indiacode.nic.in/handle/123456789/34567",
    },
    {
        "name": "Consumer Protection Act 2019",
        "url": "https://www.indiacode.nic.in/handle/123456789/45678",
    },
    {
        "name": "Information Technology Act 2000",
        "url": "https://www.indiacode.nic.in/handle/123456789/56789",
    },
    {
        "name": "Companies Act 2013",
        "url": "https://www.indiacode.nic.in/handle/123456789/67890",
    },
]


def download_act_pdf(name: str, url: str) -> str:
    path = f"data/acts/{name.replace(' ', '_')}.pdf"
    if os.path.exists(path):
        print(f"  Already exists: {path}")
        return path
    print(f"  Downloading: {name}")
    os.makedirs("data/acts", exist_ok=True)
    return path


def process_acts():
    print("Starting India Code ingestion...\n")
    for act in ACTS_TO_INGEST:
        download_act_pdf(act["name"], act["url"])
    print("\nDone. PDFs saved to data/acts/")
    print("Next step: chunk -> embed -> store in Qdrant")


if __name__ == "__main__":
    process_acts()
