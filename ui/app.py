import os
import sys
from pathlib import Path
import datetime
import streamlit as st

# Ensure we can import modules from src
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "src"))


from python.dao.money_transfer_dao import MoneyTransferDAO
from python.dao.user_dao import UserDAO
from python.ai.chatbot import ChatBot

# Initialize DAO with database path from env or fallback debug db
DB_PATH = os.getenv("DB_PATH") or str(PROJECT_ROOT / "data" / "ddl" / "debug.db")
dao = MoneyTransferDAO(db_path=DB_PATH, env=None)
user_dao = UserDAO(db_path=DB_PATH, env=None)

def get_month_savings(dao: MoneyTransferDAO, user_id: int, start_date: str, end_date: str) -> float:
    """Return net savings for a user between two dates."""
    query = (
        """
        SELECT
            COALESCE(SUM(CASE WHEN incoming = 1 THEN amount ELSE 0 END), 0) -
            COALESCE(SUM(CASE WHEN incoming = 0 THEN amount ELSE 0 END), 0)
        FROM money_transfer
        WHERE user_id = ? AND date BETWEEN ? AND ?
        """
    )
    result = dao.db_connection.execute_query(query, (user_id, start_date, end_date))
    return result[0][0] if result else 0.0

st.set_page_config(page_title="Monthly Budget", layout="centered")
page = st.sidebar.selectbox("Seleziona la pagina", ["Homepage", "Chat"])

if page == "Homepage":
    st.title("Risparmi del mese")
    users = user_dao.get_all_users()
    user_options = {f"{u[1]} (id:{u[0]})": u[0] for u in users}
    if not user_options:
        st.warning("Nessun utente trovato nel database")
    else:
        selected = st.selectbox("Seleziona utente", list(user_options.keys()))
        user_id = user_options[selected]

        today = datetime.date.today()
        month_start = today.replace(day=1)
        next_month = (month_start + datetime.timedelta(days=32)).replace(day=1)
        savings = get_month_savings(dao, user_id, month_start.isoformat(), next_month.isoformat())

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
            <div class=\"savings-circle\">{savings:.2f}</div>
            """,
            unsafe_allow_html=True,
        )

        # Sezione Inserisci Spesa
        if st.button("Inserisci spesa"):
            st.session_state.show_expense_form = True

        if st.session_state.get("show_expense_form", False):
            st.subheader("Aggiungi una nuova spesa")
            with st.form("expense_form"):
                amount = st.number_input("Importo (€)", min_value=0.01, step=0.01)
                description = st.text_input("Descrizione")
                category = st.selectbox("Categoria", ["Cibo", "Trasporti", "Intrattenimento", "Altro"])
                date = st.date_input("Data", value=today)
                submitted = st.form_submit_button("Salva spesa 🚀")
                if submitted:
                    dao.create_transfer(
                        user_id=user_id,
                        amount=amount,
                        description=description,
                        category_id=category,
                        date=date.isoformat(),
                        incoming=0
                    )
                    st.success("Spesa inserita correttamente!")
                    st.session_state.show_expense_form = False
                    st.experimental_rerun()

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

st.sidebar.markdown("---")
st.sidebar.subheader("Debug MoneyTransferDAO")
debug_action = st.sidebar.selectbox(
    "Scegli funzionalità",
    [
        "Inserisci una spesa",
        "Inserisci più spese",
        "Cerca una spesa",
        "Recupera tutte le spese",
        "Recupera una spesa",
        "Aggiorna una spesa",
        "Elimina una spesa"
    ]
)

if debug_action == "create_transfer":
    st.header("create_transfer")
    with st.form("create_transfer_form"):
        date = st.text_input("data (YYYY-MM-DD)", value=str(datetime.date.today()))
        amount = st.number_input("Prezzo", min_value=0.01, step=0.01)
        category_id = st.number_input("ID Categoria", min_value=1, step=1)
        user_id = st.number_input("ID Utente", min_value=1, step=1)
        description = st.text_input("Descrizione", value="")
        incoming = st.selectbox("Entrata", [0, 1])
        submitted = st.form_submit_button("Esegui create_transfer")
        if submitted:
            result = dao.create_transfer(
                date=date,
                amount=amount,
                category_id=category_id,
                user_id=user_id,
                description=description,
                incoming=incoming
            )
            st.write("Risultato:", result)

elif debug_action == "create_multiple_transfers":
    st.header("create_multiple_transfers")
    st.info("Inserisci una lista di tuple: (date, amount, category_id, user_id, description, incoming)")
    transfers_str = st.text_area("transfers (esempio: [('2025-08-19', 10.5, 1, 1, 'desc', 0)])")
    if st.button("Esegui create_multiple_transfers"):
        try:
            transfers = eval(transfers_str)
            result = dao.create_multiple_transfers(transfers)
            st.write("Risultato:", result)
        except Exception as e:
            st.error(f"Errore: {e}")

elif debug_action == "search_transaction_for_attributes":
    st.header("search_transaction_for_attributes")
    st.info("Inserisci un dizionario di attributi. Esempio: {'user_id': 1, 'amount': 10.5}")
    attrs_str = st.text_area("attributes")
    if st.button("Esegui search_transaction_for_attributes"):
        try:
            attrs = eval(attrs_str)
            result = dao.search_transaction_for_attributes(attrs)
            st.write("Risultato:", result)
        except Exception as e:
            st.error(f"Errore: {e}")

elif debug_action == "get_all_transfers":
    st.header("get_all_transfers")
    if st.button("Esegui get_all_transfers"):
        result = dao.get_all_transfers()
        st.write("Risultato:", result)

elif debug_action == "get_transfer_by_id":
    st.header("get_transfer_by_id")
    transfer_id = st.number_input("transfer_id", min_value=1, step=1)
    if st.button("Esegui get_transfer_by_id"):
        result = dao.get_transfer_by_id(transfer_id)
        st.write("Risultato:", result)

elif debug_action == "update_transfer":
    st.header("update_transfer")
    with st.form("update_transfer_form"):
        transfer_id = st.number_input("transfer_id", min_value=1, step=1)
        date = st.text_input("date (YYYY-MM-DD)", value="")
        amount = st.text_input("amount", value="")
        category_id = st.text_input("category_id", value="")
        user_id = st.text_input("user_id", value="")
        description = st.text_input("description", value="")
        incoming = st.text_input("incoming", value="")
        submitted = st.form_submit_button("Esegui update_transfer")
        if submitted:
            kwargs = {}
            if date: kwargs["date"] = date
            if amount: kwargs["amount"] = float(amount)
            if category_id: kwargs["category_id"] = int(category_id)
            if user_id: kwargs["user_id"] = int(user_id)
            if description: kwargs["description"] = description
            if incoming: kwargs["incoming"] = int(incoming)
            result = dao.update_transfer(transfer_id, **kwargs)
            st.write("Risultato:", result)

elif debug_action == "delete_transfer":
    st.header("delete_transfer")
    transfer_id = st.number_input("transfer_id", min_value=1, step=1)
    if st.button("Esegui delete_transfer"):
        result = dao.delete_transfer(transfer_id)
        st.write("Risultato:", result)
