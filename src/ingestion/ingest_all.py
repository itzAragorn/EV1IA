import os
import glob
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

CHROMA_DIR = "./.chroma_db"

load_dotenv()
def load_documents():
    docs = []

    # CSV
    for file in glob.glob("data/**/*.csv", recursive=True):
        loader = CSVLoader(file_path=file, encoding="utf-8")
        docs.extend(loader.load())

    return docs

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs)

def build_vectorstore(docs):
    embeddings = OpenAIEmbeddings(
        openai_api_base=os.getenv("OPENAI_EMBEDDINGS_URL"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),  # ✅ corregido
        model="text-embedding-3-small"
    )
    db = Chroma.from_documents(docs, embeddings, persist_directory=CHROMA_DIR)
    db.persist()
    return db

if __name__ == "__main__":
    print("🔄 Ingestando documentos...")
    docs = load_documents()
    print(f"Total docs: {len(docs)}")
    chunks = chunk_documents(docs)
    print(f"Total chunks: {len(chunks)}")
    build_vectorstore(chunks)
    print("✅ Vectorstore creado en", CHROMA_DIR)