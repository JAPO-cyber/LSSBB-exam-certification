import streamlit as st
import pandas as pd
from kmodes.kprototypes import KPrototypes
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram

# Dati per il DataFrame
data = {
    "Tipologia Muletto": [
        "Elettrico 3 Ruote", "Elettrico 4 Ruote", "Diesel 3 Ton", "Diesel 5 Ton",
        "Gas GPL 2 Ton", "Gas GPL 3.5 Ton", "Transpallet Elettrico", "Reach Truck",
        "Stoccatore Manuale", "Muletto Retrattile"
    ],
    "Capacità (Ton)": [1.5, 2.0, 3.0, 5.0, 2.0, 3.5, 1.2, 1.8, 0.5, 2.5],
    "Altezza Massima (m)": [3.5, 4.5, 5.0, 6.0, 4.0, 4.5, 2.5, 7.0, 1.8, 8.0],
    "Tipo Alimentazione": [
        "Elettrico", "Elettrico", "Diesel", "Diesel", "Gas GPL", "Gas GPL",
        "Elettrico", "Elettrico", "Manuale", "Elettrico"
    ],
    "Consumo (kWh/Litri/h)": [1.2, 1.5, 2.8, 3.5, 1.8, 2.2, 0.8, 1.0, 0.0, 1.3],
    "Peso (Kg)": [2000, 2500, 3500, 5000, 2800, 4000, 1200, 2200, 800, 3200],
    "Anno Acquisto": [2018, 2019, 2020, 2017, 2021, 2019, 2023, 2022, 2015, 2020],
    "Ore Lavoro": [1200, 1400, 1800, 2000, 1100, 1700, 500, 800, 300, 900],
    "Stato": [
        "Buono", "Ottimo", "Buono", "Discreto", "Ottimo", "Buono",
        "Nuovo", "Buono", "Vecchio", "Buono"
    ],
    "Ultima Manutenzione": [
        "2024-06-15", "2024-03-10", "2024-09-12", "2023-12-05", "2024-01-20",
        "2024-07-30", "2024-10-01", "2024-05-14", "2023-11-11", "2024-02-18"
    ],
    "Costo Manutenzione (€)": [150, 200, 300, 450, 180, 280, 80, 120, 50, 220]
}

# Creazione del DataFrame
df = pd.DataFrame(data)

# Selezione delle colonne da utilizzare per il clustering
st.sidebar.header("Seleziona colonne per il clustering")
numerical_columns = ["Capacità (Ton)", "Altezza Massima (m)", "Consumo (kWh/Litri/h)", "Peso (Kg)", "Ore Lavoro", "Costo Manutenzione (€)"]
categorical_columns = ["Tipologia Muletto", "Tipo Alimentazione", "Stato"]
selected_numerical = st.sidebar.multiselect("Scegli colonne numeriche", numerical_columns, default=numerical_columns)
selected_categorical = st.sidebar.multiselect("Scegli colonne categoriche", categorical_columns, default=categorical_columns)

if selected_numerical or selected_categorical:
    selected_columns = selected_numerical + selected_categorical
    data_for_clustering = df[selected_columns]

    # Conversione dei dati in array NumPy
    data_array = data_for_clustering.to_numpy()

    # Identificazione degli indici delle colonne categoriche
    categorical_indices = [data_for_clustering.columns.get_loc(col) for col in selected_categorical]

    # Applicazione del clustering K-Prototypes
    kproto = KPrototypes(n_clusters=3, random_state=42)
    clusters = kproto.fit_predict(data_array, categorical=categorical_indices)
    df["Cluster"] = clusters

    # Titolo nell'app Streamlit
    st.title("Tabella Informazioni Muletti con Clustering K-Prototypes")

    # Mostra il DataFrame nella pagina Streamlit
    st.dataframe(df)

    # Visualizzazione del dendrogramma
    st.subheader("Dendrogramma del Clustering (Numerico)")
    if len(selected_numerical) >= 2:
        linkage_matrix = linkage(data_for_clustering[selected_numerical], method="ward")
        fig, ax = plt.subplots(figsize=(10, 5))
        dendrogram(linkage_matrix, labels=df["Tipologia Muletto"].values, ax=ax)
        ax.set_title("Dendrogramma del Clustering (Numerico)")
        ax.set_ylabel("Distanza")
        st.pyplot(fig)

    # Visualizzazione dei cluster
    if len(selected_numerical) >= 2:
        st.subheader("Visualizzazione dei Cluster")
        x_col, y_col = selected_numerical[:2]
        fig, ax = plt.subplots()
        scatter = ax.scatter(
            df[x_col], df[y_col], c=df["Cluster"], cmap="viridis"
        )
        for i, txt in enumerate(df["Tipologia Muletto"]):
            ax.annotate(txt, (df[x_col].iloc[i], df[y_col].iloc[i]))
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        plt.colorbar(scatter, label="Cluster")
        st.pyplot(fig)
    else:
        st.write("Seleziona almeno due colonne numeriche per visualizzare i cluster.")
else:
    st.write("Seleziona almeno una colonna per iniziare il clustering.")

