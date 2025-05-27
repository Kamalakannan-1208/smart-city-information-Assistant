from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
from parse_knowledge import load_and_chunk_knowledge

# Initialize LLM and embeddings
llm = Ollama(model="llama3")  # Chat-capable model
embedding = OllamaEmbeddings(model="nomic-embed-text")  # Embedding-only model

# Load & embed documents
documents = load_and_chunk_knowledge()
vectordb = Chroma.from_documents(documents, embedding=embedding, persist_directory="./chroma_db")
retriever = vectordb.as_retriever()

# Build RAG QA Chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
