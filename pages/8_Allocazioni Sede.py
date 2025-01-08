import streamlit as st
import pandas as pd
import io

# Configurazione della pagina
st.set_page_config(page_title="Analisi Logistica", layout="wide")

# Variabili di stato
if "road_data" not in st.session_state:
    st.session_state.road_data = None

if "calculated" not in st.session_state:
    st.session_state.calculated = False

if "allocation_started" not in st.session_state:
    st.session_state.allocation_started = False

# Tabs principali
tab1, tab2 = st.tabs(["📂 Caricamento File", "📊 Risultati Analisi"])

# Tab 1: Caricamento File
with tab1:
    st.header("Caricamento e Modifica File")

    # Caricamento dei file
    st.sidebar.header("Caricamento File")
    file1 = st.sidebar.file_uploader("Carica il file 'GS_KAR_DB_Completo.xlsx'", type=["xlsx"])
    file2 = st.sidebar.file_uploader("Carica il file 'Configurazione_sedi.xlsx'", type=["xlsx"])
    file3 = st.sidebar.file_uploader("Carica il file 'Distanze_province.xlsx'", type=["xlsx"])

    if file1 and file2 and file3:
        try:
            # Lettura file caricati
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
            
            # File 3: Distanze_province.xlsx
            st.write("### File 3: Distanze Province")
            Province = pd.read_excel(file3, sheet_name='distanze revised')
            Province['Path'] = Province['Provincia Origine'].astype(str) + '-' + Province['Provincia Arrivo'].astype(str)
            st.dataframe(Province.head(10))
            
            # Configurazione preliminare della tabella Road
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
            
            # Salva i dati nella sessione
            st.session_state.road_data = Road
            st.session_state.sedi_data = edited_sedi
            st.session_state.province_data = Province
            
        except Exception as e:
            st.error(f"Errore durante l'elaborazione: {e}")
    else:
        st.warning("Carica tutti i file richiesti per continuare.")

# Tab 2: Risultati Analisi
with tab2:
    st.header("Risultati Analisi")

    if st.session_state.road_data is not None:
        if st.button("Avvia Allocazione"):
            st.session_state.allocation_started = True
            st.success("Codice di allocazione avviato!")

        if st.session_state.allocation_started:
            if not st.session_state.calculated:
                if st.button("Calcola Allocazione"):
                    # Funzione di calcolo
                    def calcola_allocazione(Road, Province, Configurazione_sedi):
                        for colonna in Configurazione_sedi.columns[1:]:
                            colonna1 = colonna + '- Distanza Km'
                            colonna2 = colonna + '- Tempo '
                            colonna3 = colonna + '- Sede Riferimento'

                            for index, row in Road.iterrows():
                                arrivo = row['Provincia Arrivo']
                                tipo_servizio = row['Tipologia Servizio']
                                
                                # Trova le combinazioni di percorso
                                filtered_province = Province[Province['Provincia Arrivo'] == arrivo]
                                
                                if not filtered_province.empty:
                                    try:
                                        min_km_row = filtered_province.loc[filtered_province['Distanza km'].idxmin()]
                                        Road.at[index, colonna1] = min_km_row['Distanza km']
                                        Road.at[index, colonna2] = min_km_row['Durata minuti']
                                        Road.at[index, colonna3] = min_km_row['Provincia Origine']
                                    except ValueError:
                                        st.warning(f"Errore nell'allocazione per {arrivo}")
                        return Road

                    # Esegui il calcolo
                    with st.spinner("Calcolo in corso..."):
                        Road = calcola_allocazione(
                            st.session_state.road_data,
                            st.session_state.province_data,
                            st.session_state.sedi_data,
                        )
                        st.session_state.road_data = Road
                        st.session_state.calculated = True
                        st.success("Calcolo completato!")

            if st.session_state.calculated:
                st.write("### Tabella con Risultati")
                st.dataframe(st.session_state.road_data.head(10))

                # Scaricamento dei risultati
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    st.session_state.road_data.to_excel(writer, index=False, sheet_name='Risultati')
                st.download_button(
                    label="Scarica Risultati in Excel",
                    data=output.getvalue(),
                    file_name="Output_Analisi.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
    else:
        st.warning("Carica i file nella prima tab e premi il pulsante di allocazione.")

