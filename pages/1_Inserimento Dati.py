import streamlit as st
import pandas as pd

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Non sei autorizzato a visualizzare questa pagina. Accedi prima!")
    st.stop()
    
# Titolo della pagina
st.title("Inserimento Dati")

# Form per l'inserimento di dati con diversi tipi di input
with st.form("complete_form"):
    # Testo semplice
    nome = st.text_input("Nome", placeholder="Inserisci il tuo nome")

    # Numero intero
    età = st.number_input("Età", min_value=0, step=1)

    # Numero decimale
    altezza = st.number_input("Altezza (in cm)", min_value=0.0, step=0.1)

    # Casella di testo lunga
    descrizione = st.text_area("Descrizione", placeholder="Scrivi qualcosa di te...")

    # Selezione singola
    genere = st.selectbox("Genere", ["Maschio", "Femmina", "Altro"])

    # Selezione multipla
    hobby = st.multiselect(
        "Hobby", ["Sport", "Musica", "Viaggi", "Lettura", "Cucina", "Altro"]
    )

    # Slider per numeri
    soddisfazione = st.slider("Livello di soddisfazione (1-10)", min_value=1, max_value=10)

    # Data
    data_nascita = st.date_input("Data di nascita")

    # Orario
    orario_preferito = st.time_input("Orario preferito")

    # Upload file
    file = st.file_uploader("Carica un file", type=["csv", "txt", "pdf", "png", "jpg"])

    # Colore
    colore_preferito = st.color_picker("Scegli il tuo colore preferito")

    # Checkbox
    conferma = st.checkbox("Confermi che i dati inseriti sono corretti?")

# Elaborazione dati al click del pulsante
if submit_button:
    if conferma:
        st.success("Dati inviati con successo!")
        
        # Creazione di un DataFrame per visualizzare i dati
        data = {
            "Nome": nome,
            "Età": età,
            "Altezza (cm)": altezza,
            "Descrizione": descrizione,
            "Genere": genere,
            "Hobby": ", ".join(hobby),
            "Soddisfazione": soddisfazione,
            "Data di nascita": data_nascita,
            "Orario preferito": orario_preferito,
            "Colore preferito": colore_preferito,
        }
        df = pd.DataFrame([data])
        st.dataframe(df)
    else:
        st.error("Devi confermare i dati per inviarli.")

