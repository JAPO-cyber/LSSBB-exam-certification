import streamlit as st
import pandas as pd

# Titolo dell'app
st.title("Caricamento File Excel")

# Step 1: Caricamento del file
uploaded_file = st.file_uploader("Carica un file Excel", type=["xlsx"])

if uploaded_file:
    try:
        # Lettura del file Excel
        df = pd.read_excel(uploaded_file, sheet_name=None)

        # Visualizza i fogli disponibili
        st.sidebar.header("Seleziona un foglio")
        sheet = st.sidebar.selectbox("Foglio:", list(df.keys()))

        # Visualizzazione dei dati del foglio selezionato
        st.write(f"### Dati del foglio: {sheet}")
        st.dataframe(df[sheet])

    except Exception as e:
        st.error(f"Errore nella lettura del file: {e}")
else:
    st.info("Carica un file Excel per iniziare.")