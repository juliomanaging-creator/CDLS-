import streamlit as st
import os
from pathlib import Path

# --- Core Imports ---
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from send_auto_alert import send_auto_alert 

# --- Configuration ---
ROOT_DIR = Path(r"C:\Projects\CDLS knowledge base")
INDEX_PATH = ROOT_DIR / "unified_knowledge_index"

# Clean UI Setup for CDLS Integration
st.set_page_config(page_title="CDLS Audit Intelligence", layout="wide")
st.title("🛡️ CDLS Audit Intelligence System")
st.markdown("---")

# Load Brain (Index)
if INDEX_PATH.exists():
    try:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = FAISS.load_local(
            str(INDEX_PATH), 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        # Fixes AttributeError by using docstore
        chunk_count = len(vectorstore.docstore._dict)
        st.sidebar.success(f"Index Active: {chunk_count} Chunks")
    except Exception as e:
        st.error(f"Initialization Error: {e}")
else:
    st.warning("Knowledge index not found. Please run update_index.py.")

# --- Search Interface ---
query = st.text_input("🔍 Enter Audit Query (e.g., '2026 Financial Risks'):")

if query:
    # Search the 11 chunks you built
    results = vectorstore.similarity_search_with_relevance_scores(query, k=3)
    
    for doc, score in results:
        with st.container():
            st.markdown(f"**Relevance Score:** {score:.2f}")
            st.info(doc.page_content)
            
            # --- SOURCE LABEL FEATURE ---
            # Pulls the filename from the document metadata
            source_file = doc.metadata.get('source', 'Unknown Document')
            st.caption(f"📍 **Source:** {os.path.basename(source_file)}")
            st.markdown("---")

# --- CDLS Alert Sidebar ---
with st.sidebar:
    st.subheader("📢 CDLS Priority Alerts")
    sector = st.selectbox("Audit Sector", ["Financial", "Operational", "Compliance"])
    if st.button("🚀 Dispatch Email Alert"):
        if send_auto_alert(sector, "Critical"):
            st.balloons()
            st.success("Alert sent to CDLS Stakeholders!")