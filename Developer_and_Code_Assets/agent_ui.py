import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# UI Setup
st.set_page_config(page_title="AWS Agent", layout="wide")
st.title("🤖 AWS Expert Assistant")

# Sidebar
with st.sidebar:
    st.header("Settings")
    model_choice = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"], index=1)
    temp = st.slider("Temperature", 0.0, 1.0, 0.2)
    if st.button("Clear History"):
        st.session_state.messages = []

# Logic to query documentation
def ask_aws_expert(query):
    embeddings = OpenAIEmbeddings()
    # Path to where your AWS index is stored
    db = FAISS.load_local("faiss_aws_index", embeddings, allow_dangerous_deserialization=True)
    llm = ChatOpenAI(model=model_choice, temperature=temp)
    
    prompt = ChatPromptTemplate.from_template("Answer using context: {context}\n\nQuestion: {input}")
    chain = create_retrieval_chain(db.as_retriever(), create_stuff_documents_chain(llm, prompt))
    return chain.invoke({"input": query})

# Chat Logic
if "messages" not in st.session_state: st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Ask about AWS..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)
    
    with st.spinner("Thinking..."):
        res = ask_aws_expert(p)
        sources = list(set([d.metadata.get('source', 'Unknown') for d in res["context"]]))
        full_res = f"{res['answer']}\n\n**Sources:** " + ", ".join(sources)
        
    with st.chat_message("assistant"): st.markdown(full_res)
    st.session_state.messages.append({"role": "assistant", "content": full_res})
    