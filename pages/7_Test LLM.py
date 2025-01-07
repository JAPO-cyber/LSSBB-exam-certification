import streamlit as st
import pandas as pd

# Caricamento file Excel
st.title("Caricamento File Excel")

# Carica il file Excel
uploaded_file = st.file_uploader("Carica un file Excel", type=["xlsx"])

if uploaded_file:
    try:
        # Leggi il file Excel
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        
        # Mostra il dataframe
        st.success("File caricato con successo!")
        st.write("Anteprima dei dati:")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Errore nel caricamento del file: {e}")
else:
    st.info("Carica un file Excel per visualizzarne i contenuti.")