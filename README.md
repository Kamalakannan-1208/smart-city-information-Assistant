<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FFD90F?style=for-the-badge&logo=chroma&logoColor=black)
![Groq](https://img.shields.io/badge/Groq-Black?style=for-the-badge&logo=groq&logoColor=white)

# 🏙️ Smart City Information Assistant

**AI-powered city information chatbot using RAG (Retrieval-Augmented Generation)**

[Live Demo](https://smart-city-information-assistant-fr.vercel.app/) | [Report Issues](https://github.com/Kamalakannan-1208/smart-city-information-Assistant/issues)

</div>

---

## 📋 Overview

RAG-powered city info chatbot using:
- **LLM**: Groq `llama-3.1-8b-instant` (fast, free tier available)
- **Embeddings**: `BAAI/bge-small-en-v1.5` via `fastembed` (ONNX, lightweight)
- **Vector store**: ChromaDB
- **Backend**: FastAPI
- **Frontend**: Plain HTML/CSS

---

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git
- Groq API key (get free key at https://console.groq.com)

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd smart-city-information-Assistant


# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root and add your Groq API key:

```bash
# Copy the example or create manually
echo GROQ_API_KEY=your_groq_api_key_here > .env
```

Or edit `.env` file directly:

```env
GROQ_API_KEY=your_groq_api_key_here
```

You can also customize other settings in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | (required) |
| `GROQ_MODEL` | LLM model name | `llama-3.1-8b-instant` |
| `TEMPERATURE` | LLM temperature | `0.2` |
| `MAX_TOKENS` | Max response tokens | `512` |
| `EMBEDDING_MODEL` | Embedding model | `BAAI/bge-small-en-v1.5` |
| `CHROMA_DB_DIR` | Vector DB directory | `chroma_db` |
| `KNOWLEDGE_FILE` | Knowledge base file | `knowledge.json` |
| `CHUNK_SIZE` | Text chunk size | `500` |
| `CHUNK_OVERLAP` | Chunk overlap | `50` |
| `RETRIEVER_K` | Documents to retrieve | `4` |

---

## 🖥️ Running Locally

### Start the Backend Server

```bash
uvicorn api.main:app --reload --port 8000
```

### Open the Frontend

Open `public/index.html` directly in your browser, or serve it with a simple HTTP server:

```bash
# Python 3
python -m http.server 3000 -d public
```

Then open http://localhost:3000 in your browser.

> API documentation available at: http://localhost:8000/docs

---

## 🌐 Live Demo

Check out the hosted version: https://smart-city-information-assistant-fr.vercel.app/

---

## 📁 Project Structure

```
smart-city-v2/
├── api/
│   ├── __init__.py
│   └── rag_pipeline.py  # Groq LLM + fastembed + ChromaDB
├── public/
│   └── index.html       # HTML frontend
├── chroma_db/           # Persisted vector store (auto-created)
├── knowledge.json      # City knowledge base
├── main.py      
├── requirements.txt     # Python dependencies
├── vercel.json          # Vercel routing config
├── .env                 # Environment variables (create from template)
└── README.md
```

---

## 📡 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/api/health` | Health check + model info |
| `POST` | `/api/query`  | `{ "question": "..." }` → `{ "answer": "..." }` |
| `GET`  | `/api/search?q=...` | Returns raw retrieved chunks |