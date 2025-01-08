import streamlit as st
import pandas as pd

# Configura la pagina
st.set_page_config(page_title="Analisi Logistica", layout="wide")

# Titolo principale
st.title("Analisi Logistica - Caricamento e Modifica File")

# Caricamento dei file
st.sidebar.header("Caricamento File")
file1 = st.sidebar.file_uploader("Carica il file 'GS_KAR_DB_Completo.xlsx'", type=["xlsx"])
file2 = st.sidebar.file_uploader("Carica il file 'Configurazione_sedi.xlsx'", type=["xlsx"])
file3 = st.sidebar.file_uploader("Carica il file 'Distanze_province.xlsx'", type=["xlsx"])

if file1 and file2 and file3:
    try:
        # Lettura dei file Excel
        st.subheader("Visualizzazione Dati")
        
        # File 1: GS_KAR_DB_Completo.xlsx
        st.write("### File 1: GS_KAR_DB_Completo")
        Original_Road = pd.read_excel(file1, sheet_name='Foglio1')
        Original_Road["Provincia Partenza"] = Original_Road["Provincia_Partenza_Corretta"]
        Original_Road["Provincia Arrivo"] = Original_Road["Sede_arrivo_corretta"]
        Original_Road["Tipologia Servizio"] = Original_Road["Tipologia Contratto"]
        st.dataframe(Original_Road.head(10))
        
        # File 2: Configurazione_sedi.xlsx
        st.write("### File 2: Configurazione Sedi - Modifica Interattiva")
        Configurazione_sedi = pd.read_excel(file2, sheet_name='Configurazione_scenari')
        edited_sedi = st.data_editor(Configurazione_sedi, use_container_width=True, num_rows="dynamic")
        
        # Salvataggio modifiche
        if st.button("Salva Modifiche a 'Configurazione sedi'"):
            edited_sedi.to_excel("Configurazione_sedi_modificato.xlsx", index=False)
            st.success("File salvato come 'Configurazione_sedi_modificato.xlsx'")
        
        # File 3: Distanze_province.xlsx
        st.write("### File 3: Distanze Province")
        Province = pd.read_excel(file3, sheet_name='distanze revised')
        Province['Path'] = Province['Provincia Origine'].astype(str) + '-' + Province['Provincia Arrivo'].astype(str)
        st.dataframe(Province.head(10))
        
        # Configurazione preliminare
        st.subheader("Configurazione Preliminare")
        Road = Original_Road[['Provincia Partenza', 'Provincia Arrivo', 'Tipologia Servizio']].copy()
        Road = Road.drop_duplicates()
        Road['Path_originale'] = Road['Provincia Partenza'].astype(str) + '-' + Road['Provincia Arrivo'].astype(str)
        Road['Distanza Baseline'] = None
        Road['Tempo Baseline'] = None
        
        # Aggiunta colonne per scenari
        for colonna in edited_sedi.columns[1:]:
            colonna1 = colonna + '- Distanza Km'
            colonna2 = colonna + '- Tempo '
            colonna3 = colonna + '- Sede Riferimento'
            Road[colonna1] = None
            Road[colonna2] = None
            Road[colonna3] = None
        
        st.write("### Configurazione della tabella Road")
        st.dataframe(Road.head(10))
        
    except Exception as e:
        st.error(f"Errore durante l'elaborazione: {e}")
else:
    st.warning("Carica tutti i file richiesti per continuare.")
