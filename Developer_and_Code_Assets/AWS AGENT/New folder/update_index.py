import os
import warnings
from dotenv import load_dotenv

# Silence Pydantic 3.14 warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

def build_knowledge_base():
    # 1. Load the files
    print("📂 Step 1: Loading your AWS markdown files...")
    if not os.path.exists("./aws_knowledge_base") or not os.listdir("./aws_knowledge_base"):
        print("❌ Error: 'aws_knowledge_base' is empty! Add your .md files first.")
        return

    loader = DirectoryLoader("./aws_knowledge_base", glob="**/*.md", loader_cls=TextLoader)
    raw_documents = loader.load()
    print(f"✅ Loaded {len(raw_documents)} documents.")

    # 2. Split text into chunks (Better for AI retrieval)
    print("✂️ Step 2: Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    documents = text_splitter.split_documents(raw_documents)
    print(f"✅ Created {len(documents)} text chunks.")

    # 3. Create Vector Database
    print("🧠 Step 3: Generating embeddings and building index (this uses OpenAI API)...")
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)

    # 4. Save locally
    print("💾 Step 4: Saving index to 'faiss_aws_index'...")
    vectorstore.save_local("faiss_aws_index")
    print("\