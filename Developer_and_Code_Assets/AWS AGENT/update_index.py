import os
from pathlib import Path

# --- Core LangChain Imports (Fixes Undefined errors) ---
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

# --- Configuration ---
ROOT_DIR = Path(r"C:\Projects\AWS AGENT")
KB_DIR = ROOT_DIR / "knowledge_base"
INDEX_PATH = ROOT_DIR / "unified_knowledge_index"

def build_unified_index():
    print("🧠 Starting 2026 Audit Index Update...")
    if not KB_DIR.exists():
        print(f"❌ Error: Folder not found at {KB_DIR}")
        return

    # 1. Load Documents
    loader = DirectoryLoader(str(KB_DIR), glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    
    if not documents:
        print("❌ No documents found. Please add .md files.")
        return

    # 2. Split and Create Vector Store
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    splits = text_splitter.split_documents(documents)
    print(f"📄 Documents split into {len(splits)} chunks.")

    # 3. Create Embeddings & Save Index
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = FAISS.from_documents(splits, embeddings)
    vectorstore.save_local(str(INDEX_PATH))
    print(f"✅ Success! Brain created at: {INDEX_PATH}")

if __name__ == "__main__":
    build_unified_index()