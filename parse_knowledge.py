import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

def load_and_chunk_knowledge(json_path='knowledge.json'):
    with open(json_path, 'r') as f:
        data = json.load(f)

    documents = []

    def extract_text(obj, prefix=""):
        """Recursively extract text from nested dicts/lists"""
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

    raw_chunks = extract_text(data)

    # Join chunks into large content blocks
    combined_text = "\n".join(raw_chunks)

    # Split into LangChain documents
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    doc_chunks = splitter.create_documents([combined_text])

    return doc_chunks
