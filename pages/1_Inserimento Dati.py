import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Percorso del file CSV
file_path = os.path.join("data", "1_Input Dati.csv")

# Funzione per caricare i dati dal file
def load_data():
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error(f"Il file {file_path} non esiste. Assicurati che sia presente nella directory specificata.")
        return pd.DataFrame(columns=["Nome", "Età", "Altezza (cm)", "Descrizione", "Genere", "Hobby", "Soddisfazione", "Fermi", "Giorno", "Durata", "Ora Orologio"])

# Funzione per salvare i dati nel file
def save_data(df):
    try:
        df.to_csv(file_path, index=False)
        st.success(f"File salvato con successo in: {file_path}")
    except Exception as e:
        st.error(f"Errore durante il salvataggio del file: {e}")

# Creazione delle schede
tabs = st.tabs(["Nuovo Dato", "Modifica Dati", "Scarica CSV"])

# Scheda 1: Nuovo Dato
with tabs[0]:
    st.title("Inserimento Nuovo Dato")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Dati Tradizionali")
        nome = st.text_input("Nome", placeholder="Inserisci il tuo nome")
        età = st.number_input("Età", min_value=0, step=1)
        altezza = st.number_input("Altezza (in cm)", min_value=0.0, step=0.1)
        descrizione = st.text_area("Descrizione", placeholder="Scrivi qualcosa di te...")
        genere = st.selectbox("Genere", ["Maschio", "Femmina", "Altro"])
        hobby = st.multiselect("Hobby", ["Sport", "Musica", "Viaggi", "Lettura", "Cucina", "Altro"])
        soddisfazione = st.slider("Livello di soddisfazione (1-10)", min_value=1, max_value=10)

        # Campo "Giorno" con HTML personalizzato
        st.subheader("Giorno")
        giorno_html = f"""
        <label for="giorno" style="font-size: 16px; color: white;">Seleziona Giorno:</label>
        <input type="date" id="giorno" value="{datetime.today().strftime('%Y-%m-%d')}" style="font-size: 18px; padding: 5px; background-color: black; color: white; border: 1px solid white; border-radius: 4px;">
        <script>
            const dateInput = document.getElementById('giorno');
            dateInput.addEventListener('change', (event) => {{
                const selectedDate = event.target.value.split('-').reverse().join('/');
                console.log("Data selezionata:", selectedDate);
            }});
        </script>
        """
        giorno = st.components.v1.html(giorno_html, height=70)

        durata = st.number_input("Durata (minuti)", min_value=0, step=1)

    with col2:
        st.subheader("Fermi Dinamici")
        if "fermi" not in st.session_state:
            st.session_state.fermi = []

        col3, col4 = st.columns(2)
        with col3:
            add_button = st.button("Aggiungi Fermo")
        with col4:
            remove_button = st.button("Rimuovi Fermo")

        if add_button:
            st.session_state.fermi.append("")
        if remove_button and len(st.session_state.fermi) > 0:
            st.session_state.fermi.pop()

        for i in range(len(st.session_state.fermi)):
            st.session_state.fermi[i] = st.text_input(f"Fermo {i+1}", value=st.session_state.fermi[i], key=f"fermo_{i}")

    with st.form("complete_form"):
        conferma = st.checkbox("Confermi che i dati inseriti sono corretti?")
        submit_button = st.form_submit_button("Invia")

    if submit_button:
        if conferma:
            st.success("Dati inviati con successo!")
            # Elaborazione finale per il salvataggio può essere aggiunta qui

# Scheda 3: Scarica CSV
with tabs[2]:
    st.title("Scarica CSV")

    df = load_data()
    if df.empty:
        st.warning("Non ci sono dati disponibili per il download.")
    else:
        st.write("Anteprima del file CSV:")
        st.dataframe(df)

        # Scarica il file CSV
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Scarica CSV",
            data=csv_data,
            file_name="1_Input Dati.csv",
            mime="text/csv"
        )




