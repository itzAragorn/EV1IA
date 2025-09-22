import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from src.chains.rag_chain import get_rag_chain

load_dotenv()

app = FastAPI()
rag_chain = get_rag_chain()

class Query(BaseModel):
    q: str

@app.post("/query")
def query_rag(body: Query):
    result = rag_chain.invoke({"query": body.q})
    return {"answer": result["result"]}
