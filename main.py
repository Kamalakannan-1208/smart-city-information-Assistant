import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.rag_pipeline import answer_question, retriever, GROQ_MODEL, EMBEDDING_MODEL

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Smart City Information Assistant API")

# Allow the HTML frontend (any origin) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class QueryInput(BaseModel):
    question: str


@app.get("/api/health")
def health():
    return {"status": "ok", "model": GROQ_MODEL, "embedding": EMBEDDING_MODEL}


@app.post("/api/query")
def query(body: QueryInput):
    try:
        answer = answer_question(body.question)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/search")
def search(q: str):
    try:
        docs = retriever.invoke(q)
        return {"chunks": [d.page_content for d in docs]}
    except Exception as e:
        return {"error": str(e)}

