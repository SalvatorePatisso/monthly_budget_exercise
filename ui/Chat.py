import os
import sys
from pathlib import Path
import streamlit as st

# Assicura l'import dei moduli da src
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "src"))

from python.ai.chatbot import ChatBot

def main():
    st.title("Chat con LLM")
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = ChatBot(system_message="Sei un assistente per il budget mensile.")

    # Mostra la cronologia
    for msg in st.session_state.chatbot.history[1:]:
        if msg["role"] == "user":
            st.markdown(f"**Tu:** {msg['content']}")
        else:
            st.markdown(f"**Bot:** {msg['content']}")

    user_input = st.text_input("Scrivi qui", key="chat_input")
    if st.button("Invia") and user_input:
        st.session_state.chatbot.response(user_input)
        st.experimental_rerun()

if __name__ == "__main__":
    main()