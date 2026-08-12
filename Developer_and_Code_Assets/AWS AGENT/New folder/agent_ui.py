import streamlit as st
import os
from dotenv import load_dotenv

# Modern 2026 Import Paths
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
# Use the classic path for backwards compatibility with the chain constructor
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

st.title("🤖 AWS Expert Assistant")

# Sidebar for model settings
with st.sidebar:
    st.header("Settings")
    model_choice = st.selectbox("LLM Brain:", ["gpt-4o", "gpt-4o-mini"], index=1)
    temp = st.slider("Temperature:", 0.0, 1.0, 0.2)

def get_answer(query):
    embeddings = OpenAIEmbeddings()
    # Load the local index
    db = FAISS.load_local("faiss_aws_index", embeddings, allow_dangerous_deserialization=True)
    llm = ChatOpenAI(model=model_choice, temperature=temp)
    
    # Updated 2026 Retrieval Logic
    prompt = ChatPromptTemplate.from_template("Use this context: {context}\n\nQuestion: {input}")
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(db.as_retriever(), combine_docs_chain)
    
    return retrieval_chain.invoke({"input": query})

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about AWS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.spinner("Analyzing docs..."):
        res = get_answer(prompt)
        sources = list(set([d.metadata.get('source', 'Manual') for d in res["context"]]))
        full_res = f"{res['answer']}\n\n**Sources:** " + ", ".join(sources)
        
    with st.chat_message("assistant"):
        st.markdown(full_res)
    st.session_state.messages.append({"role": "assistant", "content": full_res})