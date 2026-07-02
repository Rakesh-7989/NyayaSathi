"""
Build vector store from PDFs.

Run after downloading acts:
    python -m data.scripts.build_vector_store
"""

import os
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "nyayasathi_acts"


def load_pdfs(pdf_dir: str):
    documents = []
    for fname in os.listdir(pdf_dir):
        if fname.endswith(".pdf"):
            path = os.path.join(pdf_dir, fname)
            print(f"Loading: {fname}")
            loader = PyPDFLoader(path)
            documents.extend(loader.load())
    return documents


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    return splitter.split_documents(documents)


def build_store():
    pdf_dir = "data/acts"
    if not os.path.exists(pdf_dir):
        print(f"No PDFs found in {pdf_dir}. Run ingest_acts.py first.")
        return

    print("Loading PDFs...")
    docs = load_pdfs(pdf_dir)

    print("Chunking documents...")
    chunks = chunk_documents(docs)
    print(f"Created {len(chunks)} chunks")

    print("Connecting to Qdrant...")
    client = QdrantClient(url=QDRANT_URL)

    if client.collection_exists(COLLECTION_NAME):
        print(f"Collection {COLLECTION_NAME} already exists. Skipping.")
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )

    print("Generating embeddings and storing...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    QdrantVectorStore.from_documents(
        chunks,
        embedding=embeddings,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME,
    )

    print(f"Done! {len(chunks)} chunks stored in Qdrant ({COLLECTION_NAME})")


if __name__ == "__main__":
    build_store()
