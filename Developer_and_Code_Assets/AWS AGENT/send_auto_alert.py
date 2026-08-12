import streamlit as st
import smtplib
from email.message import EmailMessage

def send_auto_alert(sector, priority):
    # This uses credentials from your .streamlit/secrets.toml file
    if "email" not in st.secrets:
        st.error("Email secrets not found!")
        return False
    # ... (rest of your email logic)
    return True