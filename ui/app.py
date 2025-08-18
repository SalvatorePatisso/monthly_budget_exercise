import os
import sys
from pathlib import Path
import datetime
import streamlit as st

# Ensure we can import modules from src
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "src"))

from python.dao.money_transfer_dao import MoneyTransferDAO
from python.ai.chatbot import ChatBot

# Initialize DAO with database path from env or fallback debug db
DB_PATH = os.getenv("DB_PATH") or str(PROJECT_ROOT / "data" / "ddl" / "debug.db")
dao = MoneyTransferDAO(db_path=DB_PATH, env=None)


def get_month_savings(dao: MoneyTransferDAO, start_date: str, end_date: str) -> float:
    """Return net savings between two dates."""
    query = (
        """
        SELECT
            COALESCE(SUM(CASE WHEN incoming = 1 THEN amount ELSE 0 END), 0) -
            COALESCE(SUM(CASE WHEN incoming = 0 THEN amount ELSE 0 END), 0)
        FROM money_transfer
        WHERE date BETWEEN ? AND ?
        """
    )
    result = dao.db_connection.execute_query(query, (start_date, end_date))
    return result[0][0] if result else 0.0


st.set_page_config(page_title="Monthly Budget", layout="centered")
page = st.sidebar.selectbox("Seleziona la pagina", ["Homepage", "Chat"])

if page == "Homepage":
    st.title("Risparmi del mese")
    today = datetime.date.today()
    month_start = today.replace(day=1)
    next_month = (month_start + datetime.timedelta(days=32)).replace(day=1)
    savings = get_month_savings(dao, month_start.isoformat(), next_month.isoformat())

    st.markdown(
        f"""
        <style>
        .savings-circle {{
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: #4CAF50;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2em;
            margin: auto;
        }}
        </style>
        <div class="savings-circle">{savings:.2f}</div>
        """,
        unsafe_allow_html=True,
    )

elif page == "Chat":
    st.title("Chat con LLM")
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = ChatBot(system_message="Sei un assistente per il budget mensile.")

    # Display history
    for msg in st.session_state.chatbot.history[1:]:
        if msg["role"] == "user":
            st.markdown(f"**Tu:** {msg['content']}")
        else:
            st.markdown(f"**Bot:** {msg['content']}")

    user_input = st.text_input("Tu", key="chat_input")
    if st.button("Invia") and user_input:
        st.session_state.chatbot.response(user_input)
        st.experimental_rerun()
