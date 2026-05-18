"""
Compatibility shim — logic has been moved into api/rag_pipeline.py.
This file is kept so any external scripts that import parse_knowledge
still work without changes.
"""
from api.rag_pipeline import load_and_chunk_knowledge  # noqa: F401
