import streamlit as st
import pandas as pd
import plotly.express as px

# Configurazione della struttura dell'app
st.set_page_config(page_title="Supply Chain Analysis", layout="wide")

# Caricamento ed elaborazione del file Excel
st.title("Analisi della Supply Chain")
uploaded_file = st.file_uploader("Carica un file Excel con i dati della supply chain", type="xlsx")

if uploaded_file:
    # Caricamento dinamico dei dati con Pandas
    excel_data = pd.ExcelFile(uploaded_file)
    st.success("File caricato con successo!")
    st.write("Fogli disponibili:", excel_data.sheet_names)
    
    # Selezione del foglio da analizzare
    sheet_name = st.selectbox("Seleziona il foglio da analizzare:", excel_data.sheet_names)
    df = excel_data.parse(sheet_name=sheet_name)
    st.write("Anteprima dei dati caricati:")
    st.dataframe(df.head())

    # Tabs per le analisi
    tab1, tab2, tab3, tab4 = st.tabs(["Analisi dei Costi", "Rischi di Approvvigionamento", "Ottimizzazione delle Scorte", "Tempi e Costi di Spedizione"])

    # Tab 1: Analisi dei Costi
    with tab1:
        st.header("Analisi dei Costi delle Materie Prime")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Spiegazione del Grafico")
            st.write("""
                Questo grafico mostra la distribuzione dei costi unitari delle materie prime.
                Permette di identificare eventuali picchi o variazioni significative nei prezzi.
            """)
        with col2:
            if "cost per unit" in df.columns:
                fig = px.histogram(df, x="cost per unit", nbins=20, title="Distribuzione dei Costi per Unità")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("La colonna 'cost per unit' non è presente nei dati.")

    # Tab 2: Rischi di Approvvigionamento
    with tab2:
        st.header("Valutazione dei Rischi di Approvvigionamento")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Spiegazione del Grafico")
            st.write("""
                Questo grafico evidenzia la distribuzione geografica dei fornitori.
                Aiuta a individuare rischi di dipendenza da una specifica area o fornitore.
            """)
        with col2:
            if "supplier_location" in df.columns:
                fig = px.histogram(df, x="supplier_location", title="Distribuzione Geografica dei Fornitori")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("La colonna 'supplier_location' non è presente nei dati.")

    # Tab 3: Ottimizzazione delle Scorte
    with tab3:
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
            if stock_columns:
                avg_stock = df[stock_columns].mean()
                avg_stock_df = pd.DataFrame(avg_stock, columns=["Stock Level"]).reset_index()
                avg_stock_df.columns = ["Year", "Stock Level"]
                fig = px.line(avg_stock_df, x="Year", y="Stock Level", title="Livelli Medi di Scorte (2010-2021)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Non ci sono colonne relative alle scorte nei dati.")

    # Tab 4: Tempi e Costi di Spedizione
    with tab4:
        st.header("Tempi di Transito e Costi di Spedizione")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Spiegazione del Grafico")
            st.write("""
                Questo grafico rappresenta i costi unitari medi per regione di approvvigionamento,
                utile per analizzare costi di trasporto e identificare eventuali anomalie.
            """)
        with col2:
            if "supplier_location" in df.columns and "cost per unit" in df.columns:
                fig = px.box(df, x="supplier_location", y="cost per unit", title="Costi per Regione")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Le colonne 'supplier_location' e 'cost per unit' non sono presenti nei dati.")