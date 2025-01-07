import streamlit as st
import pandas as pd
import plotly.express as px

# Funzione per caricare i dati
@st.cache
def load_data(file):
    return pd.ExcelFile(file)

# Configurazione della struttura dell'app
st.set_page_config(page_title="Supply Chain Analysis", layout="wide")

# Caricamento del file Excel
st.title("Analisi della Supply Chain")
uploaded_file = st.file_uploader("Carica un file Excel", type="xlsx")
if uploaded_file:
    data_file = load_data(uploaded_file)
    st.success("File caricato con successo!")
    st.write("Fogli disponibili:", data_file.sheet_names)
    df = data_file.parse(sheet_name=0)

    # Tabs
    tabs = st.tabs(["Analisi dei Costi", "Rischi di Approvvigionamento", "Ottimizzazione delle Scorte", "Tempi e Costi di Spedizione"])

    # Tab 1: Analisi dei Costi
    with tabs[0]:
        st.header("Analisi dei Costi delle Materie Prime")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Spiegazione del Grafico")
            st.write("""
                Questo grafico mostra la distribuzione dei costi unitari delle materie prime.
                Permette di identificare eventuali picchi o variazioni significative nei prezzi.
            """)
        with col2:
            fig = px.histogram(df, x="cost per unit", nbins=20, title="Distribuzione dei Costi per Unità")
            st.plotly_chart(fig, use_container_width=True)

    # Tab 2: Rischi di Approvvigionamento
    with tabs[1]:
        st.header("Valutazione dei Rischi di Approvvigionamento")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Spiegazione del Grafico")
            st.write("""
                Questo grafico evidenzia la distribuzione geografica dei fornitori.
                Aiuta a individuare rischi di dipendenza da una specifica area o fornitore.
            """)
        with col2:
            fig = px.histogram(df, x="supplier_location", title="Distribuzione Geografica dei Fornitori")
            st.plotly_chart(fig, use_container_width=True)

    # Tab 3: Ottimizzazione delle Scorte
    with tabs[2]:
        st.header("Ottimizzazione delle Scorte")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Spiegazione del Grafico")
            st.write("""
                Questo grafico mostra i livelli medi di scorte nel tempo, aiutando
                a individuare materiali con giacenze eccessive o insufficienti.
            """)
        with col2:
            stock_columns = [col for col in df.columns if "quantity" in col]
            avg_stock = df[stock_columns].mean()
            fig = px.line(avg_stock, title="Livelli Medi di Scorte (2010-2021)")
            st.plotly_chart(fig, use_container_width=True)

    # Tab 4: Tempi e Costi di Spedizione
    with tabs[3]:
        st.header("Tempi di Transito e Costi di Spedizione")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Spiegazione del Grafico")
            st.write("""
                Questo grafico rappresenta i costi unitari medi per regione di approvvigionamento,
                utile per analizzare costi di trasporto e identificare eventuali anomalie.
            """)
        with col2:
            fig = px.box(df, x="supplier_location", y="cost per unit", title="Costi per Regione")
            st.plotly_chart(fig, use_container_width=True)