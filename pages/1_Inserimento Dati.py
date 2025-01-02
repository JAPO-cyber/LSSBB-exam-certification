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

# Schede Streamlit
tabs = st.tabs(["Nuovo Dato", "Modifica Dati", "Scarica CSV"])

# Scheda 1: Nuovo Dato
with tabs[0]:
    st.title("Inserimento Nuovo Dato")

    if "fermi" not in st.session_state:
        st.session_state.fermi = []

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

        # Nuovi campi
        giorno = st.date_input("Giorno", value=datetime.today().date())
        durata = st.number_input("Durata (minuti)", min_value=0, step=1)
        ora_orologio = st.time_input("Ora Orologio", value=datetime.now().time())

    with col2:
        st.subheader("Fermi Dinamici")
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
            df_new = pd.DataFrame([{
                "Nome": nome,
                "Età": età,
                "Altezza (cm)": altezza,
                "Descrizione": descrizione,
                "Genere": genere,
                "Hobby": " -- ".join(hobby),
                "Soddisfazione": soddisfazione,
                "Fermi": " -- ".join(st.session_state.fermi),
                "Giorno": giorno,
                "Durata": durata,
                "Ora Orologio": ora_orologio
            }])

            df_existing = load_data()
            df_updated = pd.concat([df_existing, df_new], ignore_index=True)
            save_data(df_updated)
            st.success("Dati aggiunti con successo!")

# Scheda 2: Modifica Dati
with tabs[1]:
    st.title("Modifica Dati")

    df = load_data()
    if df.empty:
        st.warning("Non ci sono dati disponibili per la modifica.")
    else:
        st.write("Dati attualmente salvati:")
        st.dataframe(df)

        row_index = st.number_input("Seleziona la riga da modificare (0 per la prima)", min_value=0, max_value=len(df)-1, step=1)
        st.write("Riga selezionata:")
        st.write(df.iloc[row_index])

        with st.form("edit_form"):
            nome = st.text_input("Nome", df.iloc[row_index]["Nome"])
            età = st.number_input("Età", min_value=0, step=1, value=int(df.iloc[row_index]["Età"]))
            altezza = st.number_input("Altezza (in cm)", min_value=0.0, step=0.1, value=float(df.iloc[row_index]["Altezza (cm)"]))
            descrizione = st.text_area("Descrizione", df.iloc[row_index]["Descrizione"])
            genere = st.selectbox("Genere", ["Maschio", "Femmina", "Altro"], index=["Maschio", "Femmina", "Altro"].index(df.iloc[row_index]["Genere"]))
            hobby = st.text_area("Hobby (separati da --)", value=df.iloc[row_index]["Hobby"])
            fermi = df.iloc[row_index].get("Fermi", "")
            if pd.isna(fermi):
                fermi = ""
            fermi = st.text_area("Fermi (separati da --)", value=fermi)

            giorno = st.date_input("Giorno", value=pd.to_datetime(df.iloc[row_index]["Giorno"], errors="coerce").date() if "Giorno" in df.columns and pd.notna(df.iloc[row_index]["Giorno"]) else datetime.today().date())
            durata = st.number_input("Durata (minuti)", min_value=0, step=1, value=int(df.iloc[row_index]["Durata"]) if "Durata" in df.columns and pd.notna(df.iloc[row_index]["Durata"]) else 0)
            ora_orologio = st.time_input("Ora Orologio", value=pd.to_datetime(df.iloc[row_index]["Ora Orologio"], errors="coerce").time() if "Ora Orologio" in df.columns and pd.notna(df.iloc[row_index]["Ora Orologio"]) else datetime.now().time())

            save_button = st.form_submit_button("Salva Modifiche")

        if save_button:
            df.at[row_index, "Nome"] = nome
            df.at[row_index, "Età"] = età
            df.at[row_index, "Altezza (cm)"] = altezza
            df.at[row_index, "Descrizione"] = descrizione
            df.at[row_index, "Genere"] = genere
            df.at[row_index, "Hobby"] = hobby
            df.at[row_index, "Fermi"] = fermi
            df.at[row_index, "Giorno"] = giorno
            df.at[row_index, "Durata"] = durata
            df.at[row_index, "Ora Orologio"] = ora_orologio

            save_data(df)
            st.success("Modifiche salvate con successo!")
            st.dataframe(df)


