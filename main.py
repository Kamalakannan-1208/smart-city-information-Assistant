from fastapi import FastAPI, Query
from pydantic import BaseModel
from rag_pipeline import qa_chain, retriever

app = FastAPI()

class QueryInput(BaseModel):
    question: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/query")
def query(input: QueryInput):
    try:
        response = qa_chain.run(input.question)
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}

@app.get("/search")
def search(q: str = Query(...)):
    try:
        results = retriever.get_relevant_documents(q)
        return {"chunks": [doc.page_content for doc in results]}
    except Exception as e:
        return {"error": str(e)}
