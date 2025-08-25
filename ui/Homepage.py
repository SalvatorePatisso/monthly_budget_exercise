import os
import sys
from pathlib import Path
import datetime
import streamlit as st

# Assicura l'import dei moduli da src
PROJECT_ROOT = Path(__file__).resolve().parents[1]
print("project_root",PROJECT_ROOT)
sys.path.append(str(PROJECT_ROOT))

from src.python.dao.money_transfer_dao import MoneyTransferDAO
from src.python.dao.user_dao import UserDAO
from src.python.dao.categories_dao import CategoriesDAO

# Inizializza DAO con percorso database da env o fallback debug db
DB_PATH = os.getenv("DB_PATH") or str(PROJECT_ROOT / "data" / "ddl" / "debug.db")
dao = MoneyTransferDAO(db_path=DB_PATH, env=None)
user_dao = UserDAO(db_path=DB_PATH, env=None)

def get_month_savings(dao: MoneyTransferDAO, user_id: int, start_date: str, end_date: str) -> float:
    """Restituisce il risparmio netto di un utente tra due date."""
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

st.set_page_config(page_title="Budget Mensile", layout="centered")
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

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Inserisci una spesa"):
                st.session_state.show_expense_form = True
        with col2:
            if st.button("Cerca Spesa"):
                st.session_state.show_search_form = True
                st.session_state.search_attributes = {}
                st.session_state.search_inputs = {}

        # Form inserimento spesa
        if st.session_state.get("show_expense_form", False):
            st.subheader("Aggiungi una nuova spesa")
            with st.form("expense_form"):
                amount = st.number_input("Importo (€)", min_value=0.01, step=0.01)
                description = st.text_input("Descrizione")

                categories = CategoriesDAO(db_path=DB_PATH).get_all_categories()
                categories_name = [categories[i][1] for i in range(0,len(categories))]
                category_name = st.selectbox(label = "Categoria",options=categories_name)
                category_id = None
                for category in categories:
                    if category_name == category[1]:
                        category_id = category[0]

                date = st.date_input("Data", value=today)
                submitted = st.form_submit_button("Salva spesa 🚀")
                if submitted:
                    dao.create_transfer(
                        user_id=user_id,
                        amount=amount,
                        description=description,
                        category_id=category_id,
                        date=date.isoformat(),
                        incoming=0
                    )
                    st.success("Spesa inserita correttamente!")
                    st.session_state.show_expense_form = False
                    st.experimental_rerun()

        # Form ricerca spesa
        if st.session_state.get("show_search_form", False):
            st.subheader("Cerca una spesa")
            ATTRIBUTI = {
                "start_amount": "Importo minimo",
                "end_amount": "Importo massimo",
                "start_date": "Data inizio (YYYY-MM-DD)",
                "end_date": "Data fine (YYYY-MM-DD)",
                "amount": "Importo esatto",
                "category_id": "ID Categoria",
                "description": "Descrizione",
                "transaction_id": "ID Transazione",
                "incoming": "Entrata (0=spesa, 1=entrata)",
                "user_id": "ID Utente"
            }

            # Inizializza lo stato dei filtri se non esiste
            if "search_filters" not in st.session_state:
                st.session_state.search_filters = {}

            # Espandi per ogni filtro
            for key, label in ATTRIBUTI.items():
                with st.expander(f"Aggiungi filtro: {label}", expanded=False):
                    value = st.text_input(f"Inserisci valore per {label}", key=f"filter_{key}")
                    if value:
                        st.session_state.search_filters[key] = value

            # Mostra i filtri attivi
            if st.session_state.search_filters:
                st.info("Filtri attivi:")
                for k, v in st.session_state.search_filters.items():
                    st.write(f"{ATTRIBUTI[k]}: {v}")

            # Button per visualizzare il risultato
            if st.button("Visualizza risultato"):
                search_dict = {}
                for k, v in st.session_state.search_filters.items():
                    if v != "":
                        # Cast automatico per alcuni campi
                        if k in ["start_amount", "end_amount", "amount"]:
                            try:
                                search_dict[k] = float(v)
                            except:
                                st.warning(f"Valore non valido per {ATTRIBUTI[k]}")
                                continue
                        elif k in ["category_id", "transaction_id", "incoming", "user_id"]:
                            try:
                                search_dict[k] = int(v)
                            except:
                                st.warning(f"Valore non valido per {ATTRIBUTI[k]}")
                                continue
                        else:
                            search_dict[k] = v
                results = dao.search_transaction_for_attributes(search_dict)
                st.session_state.search_results = results

            # Mostra i risultati della ricerca
            if "search_results" in st.session_state and st.session_state.search_results:
                st.subheader("Risultati della ricerca")
                for r in st.session_state.search_results:
                    st.write(r)
                    col_upd, col_del = st.columns(2)
                    with col_upd:
                        if st.button("Aggiorna spesa", key=f"upd_{r[0]}"):
                            st.session_state.update_id = r[0]
                            st.session_state.show_update_form = True
                    with col_del:
                        if st.button("Cancella spesa", key=f"del_{r[0]}"):
                            dao.delete_transfer(r[0])
                            st.success("Spesa cancellata correttamente!")
                            st.session_state.search_results = [res for res in st.session_state.search_results if res[0] != r[0]]
                            st.experimental_rerun()

            # Form aggiornamento spesa
            if st.session_state.get("show_update_form", False):
                st.subheader("Aggiorna spesa")
                update_id = st.session_state.update_id
                spesa = dao.get_transfer_by_id(update_id)
                with st.form("update_form"):
                    new_date = st.text_input("Data", value=spesa[1])
                    new_amount = st.number_input("Importo", value=float(spesa[2]))
                    new_category_id = st.text_input("ID Categoria", value=str(spesa[3]))
                    new_user_id = st.text_input("ID Utente", value=str(spesa[4]))
                    new_description = st.text_input("Descrizione", value=spesa[5] if spesa[5] else "")
                    new_incoming = st.selectbox("Entrata", [0, 1], index=int(spesa[6]))
                    submitted_upd = st.form_submit_button("Salva modifiche")
                    if submitted_upd:
                        dao.update_transfer(
                            update_id,
                            date=new_date,
                            amount=new_amount,
                            category_id=int(new_category_id),
                            user_id=int(new_user_id),
                            description=new_description,
                            incoming=int(new_incoming)
                        )
                        st.success("Spesa aggiornata correttamente!")
                        st.session_state.show_update_form = False
                        st.experimental_rerun()

elif page == "Chat":
    # Assicura che la cartella ui sia nel sys.path
    UI_PATH = str(Path(__file__).resolve().parent)
    if UI_PATH not in sys.path:
        sys.path.append(UI_PATH)
    from Chat import main as chat_main
    chat_main()


