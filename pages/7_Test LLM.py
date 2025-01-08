import streamlit as st
import pandas as pd

# Inizializzazione session_state per salvare i dati caricati
if "data" not in st.session_state:
    st.session_state.data = []

# Tab di navigazione
tab1, tab2, tab3 = st.tabs(["Carica File", "Indici di Rotazione", "Altro"])

# Tab 1: Caricamento file
with tab1:
    st.title("Carica i File Excel")

    # Caricamento file
    uploaded_files = st.file_uploader("Carica uno o più file Excel", type=["xlsx"], accept_multiple_files=True)

    if uploaded_files:
        try:
            combined_data = []
            for uploaded_file in uploaded_files:
                # Lettura del file Excel
                sheets = pd.read_excel(uploaded_file, sheet_name=None)  # Legge tutte le sheet
                for sheet_name, sheet_data in sheets.items():
                    sheet_data['File'] = uploaded_file.name  # Aggiunge il nome del file come colonna
                    sheet_data['Sheet'] = sheet_name  # Aggiunge il nome del foglio come colonna
                    combined_data.append(sheet_data)

            # Combina tutti i dati in un unico DataFrame
            combined_df = pd.concat(combined_data, ignore_index=True)
            st.session_state.data = combined_df

            st.success("File caricati e combinati con successo!")

            # Mostra l'anteprima del file combinato
            st.write("Anteprima dei dati combinati:")
            st.dataframe(st.session_state.data.head())

            # Verifica delle colonne richieste
            required_columns = ["beginning_quantity_2011", "ending_quantity_2011"]
            missing_columns = [col for col in required_columns if col not in combined_df.columns]

            if missing_columns:
                st.warning(f"Mancano le seguenti colonne necessarie: {', '.join(missing_columns)}")

                # Opzione per accoppiare le colonne mancanti
                st.write("Accoppia le colonne del file caricato a quelle richieste:")
                column_mapping = {}
                for col in missing_columns:
                    selected_col = st.selectbox(f"Seleziona una colonna per '{col}'", options=combined_df.columns, key=col)
                    column_mapping[col] = selected_col

                if st.button("Applica Mappatura"):
                    for required, actual in column_mapping.items():
                        combined_df[required] = combined_df[actual]
                    st.success("Mappatura completata con successo! Tutte le colonne richieste sono ora presenti.")

            else:
                st.success("Tutte le colonne necessarie sono presenti.")

        except Exception as e:
            st.error(f"Errore nel caricamento dei file: {e}")
    else:
        st.info("Carica uno o più file Excel per iniziare.")

# Tab 2: Analisi Statistica
with tab2:
    if st.session_state.data is None or len(st.session_state.data) == 0:
        st.warning("Carica prima un file nella tab 'Carica File'.")
    else:
        st.title("Analisi Statistica dei Dati")

        # DataFrame di lavoro
        data = st.session_state.data

        # Calcolo delle statistiche
        summary = data.describe(include='all').transpose()
        summary['Missing Values'] = data.isnull().sum()
        summary['Data Type'] = data.dtypes
        summary['Unique Values'] = data.nunique()

        # Mostra tabella riassuntiva
        st.write("Tabella Riassuntiva delle Statistiche per Colonna:")
        st.dataframe(summary)

        # Opzione per visualizzare ulteriori dettagli
        col_name = st.selectbox("Seleziona una colonna per analisi dettagliata:", options=data.columns)

        if col_name:
            st.write(f"Analisi dettagliata per la colonna: {col_name}")

            if data[col_name].dtype in ['float64', 'int64']:
                st.write(f"Media: {data[col_name].mean()}")
                st.write(f"Mediana: {data[col_name].median()}")
                st.write(f"Deviazione Standard: {data[col_name].std()}")
                st.write(f"Quartili: {data[col_name].quantile([0.25, 0.5, 0.75]).to_dict()}")
            elif data[col_name].dtype == 'object':
                st.write("Valori univoci:")
                st.write(data[col_name].value_counts())
            else:
                st.write("Tipo di dato non supportato per analisi dettagliata.")

