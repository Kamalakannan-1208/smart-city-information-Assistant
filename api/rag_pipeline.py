import os
import json
from typing import List
from dotenv import load_dotenv

from groq import Groq
from fastembed import TextEmbedding

from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

# Load environment variables from .env file
load_dotenv()


# ─────────────────────────────────────────────────────
# Configuration from environment
# ─────────────────────────────────────────────────────
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "chroma_db")
KNOWLEDGE_FILE = os.getenv("KNOWLEDGE_FILE", "knowledge.json")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
RETRIEVER_K = int(os.getenv("RETRIEVER_K", "2"))
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "512"))


# ─────────────────────────────────────────────────────
# FastEmbed Wrapper
# ─────────────────────────────────────────────────────
class FastEmbedWrapper(Embeddings):

    def __init__(self, model_name: str = None):
        if model_name is None:
            model_name = EMBEDDING_MODEL
        self.model = TextEmbedding(model_name=model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.embed(texts)
        return [vec.tolist() for vec in embeddings]

    def embed_query(self, text: str) -> List[float]:
        embedding = next(self.model.embed([text]))
        return embedding.tolist()


# ─────────────────────────────────────────────────────
# Load Knowledge Base
# ─────────────────────────────────────────────────────
def load_and_chunk_knowledge(
    json_path: str = None
) -> List[Document]:

    if json_path is None:
        json_path = KNOWLEDGE_FILE

    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, "..", json_path)

    with open(full_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    def extract_text(obj, prefix=""):
        texts = []

        if isinstance(obj, dict):
            for key, value in obj.items():
                new_prefix = f"{prefix} {key}".strip()
                texts.extend(extract_text(value, new_prefix))

        elif isinstance(obj, list):
            for item in obj:
                texts.extend(extract_text(item, prefix))

        elif isinstance(obj, str):
            texts.append(f"{prefix}: {obj}")

        return texts

    raw_text = "\n".join(extract_text(data))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    documents = splitter.create_documents([raw_text])

    return documents


# ─────────────────────────────────────────────────────
# Vector DB
# ─────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHROMA_DIR = os.path.join(BASE_DIR, "..", CHROMA_DB_DIR)

embedding = FastEmbedWrapper()

if os.path.exists(CHROMA_DIR):

    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding
    )

else:

    documents = load_and_chunk_knowledge()

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embedding,
        persist_directory=CHROMA_DIR
    )

retriever = vectordb.as_retriever(
    search_kwargs={"k": RETRIEVER_K}
)


# ─────────────────────────────────────────────────────
# Groq Client
# ─────────────────────────────────────────────────────
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found")

groq_client = Groq(api_key=groq_api_key)


# ─────────────────────────────────────────────────────
# QA Function
# ─────────────────────────────────────────────────────
def answer_question(question: str) -> str:

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    system_prompt = f"""
You are a Smart City Information Assistant.

Answer ONLY using the provided context.

If information is unavailable in the context,
say you do not know.

CONTEXT:
{context}
"""

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )

    return response.choices[0].message.content