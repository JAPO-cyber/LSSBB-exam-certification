import streamlit as st
import pandas as pd

# Inizializzazione session_state per salvare i dati caricati
if "data" not in st.session_state:
    st.session_state.data = None

# Tab di navigazione
tab1, tab2, tab3 = st.tabs(["Carica File", "Analisi Statistica", "Altro"])

# Tab 1: Caricamento file
with tab1:
    st.title("Carica il File Excel")

    # Caricamento file
    uploaded_file = st.file_uploader("Carica un file Excel", type=["xlsx"])

    if uploaded_file:
        try:
            # Lettura del file Excel
            st.session_state.data = pd.read_excel(uploaded_file, sheet_name="MOCK_DATA (3)")
            st.success("File caricato con successo!")
            st.write("Anteprima dei dati:")
            st.dataframe(st.session_state.data.head())
        except Exception as e:
            st.error(f"Errore nel caricamento del file: {e}")

# Tab 2: Analisi Statistica
with tab2:
    if st.session_state.data is None:
        st.warning("Carica prima un file nella tab 'Carica File'.")
    else:
        st.title("Analisi Statistica")

        # Descrizione dei dati contenuti
        st.subheader("Descrizione del dataset")
        st.markdown("""
        Questo dataset contiene informazioni relative alla gestione delle scorte e ai fornitori. 
        Ecco una descrizione di alcune colonne principali:
        - **raw_material_id**: ID univoco del materiale grezzo.
        - **description**: Tipo di materiale (es. plastica, cemento).
        - **supplier**: Nome del fornitore.
        - **supplier_location**: Località del fornitore.
        - **cost per unit**: Costo per unità di materiale.
        - **beginning_quantity_2021**: Quantità iniziale per l'anno 2021.
        - **ending_quantity_X**: Quantità finale per diversi anni (2010-2021).
        """)

        # Calcolo delle statistiche descrittive
        stats = st.session_state.data.describe(include='all').transpose()
        stats['missing_values'] = st.session_state.data.isnull().sum()  # Valori mancanti
        stats['unique_values'] = st.session_state.data.nunique()  # Valori unici

        # Rinomina delle colonne
        stats.rename(columns={
            'count': 'Numero di Dati',
            'mean': 'Media',
            'std': 'Deviazione Standard',
            'min': 'Valore Minimo',
            '25%': '25° Percentile',
            '50%': 'Mediana',
            '75%': '75° Percentile',
            'max': 'Valore Massimo'
        }, inplace=True)

        # Mostra i dati in una tabella
        st.subheader("Statistiche Descrittive")
        st.dataframe(stats)

        # Opzione per scaricare le statistiche
        st.download_button(
            label="Scarica Statistiche come CSV",
            data=stats.to_csv().encode('utf-8'),
            file_name='statistiche_colonne.csv',
            mime='text/csv'
        )

# Tab 3: Altro
with tab3:
    if st.session_state.data is None:
        st.warning("Carica prima un file nella tab 'Carica File'.")
    else:
        st.title("Altro")
        st.write("Aggiungi qui altre funzionalità personalizzate.")