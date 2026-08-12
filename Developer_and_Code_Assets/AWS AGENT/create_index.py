import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader

# Load environment variables (API Key)
load_dotenv()

def create_local_db():
    print("📂 Loading documents...")
    # Updated loader logic for 2026 compatibility
    loader = DirectoryLoader("./aws_knowledge_base", glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()

    print(f"🧠 Creating index for {len(documents)} files...")
    embeddings = OpenAIEmbeddings()
    
    # Create the searchable index
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    # Save it locally
    vectorstore.save_local("faiss_aws_index")
    print("✅ Search index created successfully in 'faiss_aws_index' folder!")

if __name__ == "__main__":
    create_local_db()
    