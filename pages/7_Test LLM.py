import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Inizializzazione session_state per salvare i dati caricati
if "data" not in st.session_state:
    st.session_state.data = None

# Tab di navigazione
tab1, tab2, tab3 = st.tabs(["Carica File", "Indici di Rotazione", "Altro"])

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

# Tab 2: Calcolo indici di rotazione del magazzino
with tab2:
    if st.session_state.data is None:
        st.warning("Carica prima un file nella tab 'Carica File'.")
    else:
        st.title("Indici di Rotazione del Magazzino")

        # Filtriamo le colonne necessarie
        data = st.session_state.data.copy()
        try:
            # Identifica le colonne per gli anni dal 2011 in avanti
            years = [col for col in data.columns if "ending_quantity_" in col and int(col.split("_")[-1]) >= 2011]

            # Calcolo degli indici di rotazione per ogni anno
            rotation_data = []
            for year in years:
                year_int = int(year.split("_")[-1])
                beginning_col = f"beginning_quantity_{year_int}" if f"beginning_quantity_{year_int}" in data.columns else None

                if beginning_col:
                    # Calcolo del consumo medio e magazzino medio
                    data['Consumo_Annuo'] = (data[beginning_col] - data[year]).abs()
                    data['Magazzino_Medio'] = (data[beginning_col] + data[year]) / 2
                    data['Indice_Rotazione'] = (data['Consumo_Annuo'] / data['Magazzino_Medio']).round(2)

                    # Aggiunge i dati per l'anno corrente
                    rotation_data.append(data[['raw_material_id', 'supplier', 'Consumo_Annuo', 'Magazzino_Medio', 'Indice_Rotazione']].assign(Anno=year_int))

            # Combina i risultati per tutti gli anni
            rotation_df = pd.concat(rotation_data)

            # Mostra i risultati in tabella
            st.write("Tabella con gli indici di rotazione del magazzino per tutti gli anni:")
            st.dataframe(rotation_df)

            # Grafico a linee: Indice di rotazione per anno e materiale
            st.subheader("Grafico: Indici di Rotazione per Anno e Materiale")
            fig, ax = plt.subplots(figsize=(12, 6))
            for material in rotation_df['raw_material_id'].unique():
                subset = rotation_df[rotation_df['raw_material_id'] == material]
                ax.plot(subset['Anno'], subset['Indice_Rotazione'], label=material)

            ax.set_title("Indici di Rotazione per Anno e Materiale")
            ax.set_ylabel("Indice di Rotazione")
            ax.set_xlabel("Anno")
            ax.legend(title="Materiale", bbox_to_anchor=(1.05, 1), loc='upper left')
            st.pyplot(fig)

            # Grafico a barre: Consumo annuo totale per fornitore
            st.subheader("Grafico: Consumo Annuo Totale per Fornitore")
            consumo_fornitori = rotation_df.groupby('supplier')['Consumo_Annuo'].sum().sort_values(ascending=False)
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            consumo_fornitori.plot(kind='bar', ax=ax2)
            ax2.set_title("Consumo Annuo Totale per Fornitore")
            ax2.set_ylabel("Consumo Annuo")
            ax2.set_xlabel("Fornitore")
            plt.xticks(rotation=45)
            st.pyplot(fig2)

            # Opzione per scaricare la tabella con i calcoli
            st.download_button(
                label="Scarica i risultati come CSV",
                data=rotation_df.to_csv(index=False).encode('utf-8'),
                file_name='indici_rotazione_magazzino.csv',
                mime='text/csv'
            )
        except KeyError as e:
            st.error(f"Errore: manca la colonna necessaria per il calcolo ({e}).")

# Tab 3: Altro
with tab3:
    if st.session_state.data is None:
        st.warning("Carica prima un file nella tab 'Carica File'.")
    else:
        st.title("Altro")
        st.write("Aggiungi qui altre funzionalità personalizzate.")