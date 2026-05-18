# 🏙️ Smart City Information Assistant

RAG-powered city info chatbot using:
- **LLM**: Groq `llama-3.1-8b-instant` (fast, free tier available)
- **Embeddings**: `BAAI/bge-small-en-v1.5` via `fastembed` (ONNX, lightweight)
- **Vector store**: ChromaDB (local persistent)
- **Backend**: FastAPI
- **Frontend**: Plain HTML/CSS/JS (no framework needed)
- **Hosting**: Vercel

---

## Project Structure

```
├── api/
│   ├── __init__.py
│   ├── main.py          # FastAPI app (Vercel serverless entry point)
│   └── rag_pipeline.py  # Groq LLM + fastembed + ChromaDB
├── public/
│   └── index.html       # HTML frontend
├── chroma_db/           # Persisted vector store (auto-created)
├── knowledge.json       # City knowledge base
├── requirements.txt
├── vercel.json          # Vercel routing config
└── README.md
```

---

## Local Development

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set your Groq API key

Get a free key at https://console.groq.com

```bash
export GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

### 3. Run the FastAPI backend

```bash
uvicorn api.main:app --reload --port 8000
```

### 4. Open the frontend

Open `public/index.html` directly in your browser.
The frontend auto-detects `localhost` and points to `http://localhost:8000`.

> API docs available at: http://localhost:8000/docs

---

## Deploy to Vercel

### 1. Install Vercel CLI (optional)

```bash
npm i -g vercel
```

### 2. Set the environment variable in Vercel dashboard

`Settings → Environment Variables → Add`

| Name | Value |
|------|-------|
| `GROQ_API_KEY` | `gsk_xxxxxxxxxxxxxxxxxxxx` |

### 3. Deploy

```bash
vercel --prod
```

Vercel routes:
- `/api/*` → FastAPI serverless function
- `/*`     → `public/index.html`

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/api/health` | Health check + model info |
| `POST` | `/api/query`  | `{ "question": "..." }` → `{ "answer": "..." }` |
| `GET`  | `/api/search?q=...` | Returns raw retrieved chunks |
