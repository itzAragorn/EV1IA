# src/chains/rag_chain.py
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma

CHROMA_DIR = "./.chroma_db"

def get_rag_chain():
    # embeddings
    embeddings = OpenAIEmbeddings(
        openai_api_base=os.getenv("OPENAI_EMBEDDINGS_URL"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),  # ✅ usa la variable correcta
        model="text-embedding-3-small"
    )

    # vectorstore
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 4})

    # LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.2,
        openai_api_base=os.getenv("OPENAI_BASE_URL"),
        openai_api_key=os.getenv("OPENAI_API_KEY")  # ✅ igual aquí
    )

    # Prompt
    prompt = PromptTemplate(
        template="""Eres un asistente para la empresa CleanPro.
Usa solo la evidencia provista para responder en español.
Pregunta: {question}
Evidencia:
{context}
---
Si la evidencia es insuficiente, dilo claramente.
Responde siempre con la fuente al final.""",
        input_variables=["question", "context"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain
