import os
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# Verified Config
ROOT_DIR = Path(r"C:\Projects\AWS AGENT")
KB_DIR = ROOT_DIR / "knowledge_base"
INDEX_PATH = ROOT_DIR / "unified_knowledge_index"

def build_2026_index():
    print(f"📂 Scanning Knowledge Base at: {KB_DIR}")
    # Load all MD files (including legal/privacy_v1.md)
    loader = DirectoryLoader(str(KB_DIR), glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    
    if not documents:
        print("❌ No files found! Check your folder structure.")
        return

    # 2026 Standard Chunking
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    print(f"📄 Found {len(documents)} files. Split into {len(docs)} chunks.")

    # Embeddings (Requires 'ollama pull nomic-embed-text' first)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Save the local search database
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(str(INDEX_PATH))
    print("✅ Search Index Built Successfully!")

if __name__ == "__main__":
    build_2026_index()