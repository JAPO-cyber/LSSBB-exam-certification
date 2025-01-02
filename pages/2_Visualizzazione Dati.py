import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Percorso del file CSV
file_path = os.path.join("data", "1_Input Dati.csv")

# Funzione per caricare i dati
def load_data():
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error(f"Il file {file_path} non esiste. Assicurati che sia presente nella directory specificata.")
        return pd.DataFrame(columns=["Nome", "Età", "Altezza (cm)", "Descrizione", "Genere", "Hobby", "Soddisfazione", "Fermi", "Giorno", "Durata", "Ora Orologio"])

# Titolo dell'app
st.title("Analisi dei Dati Inseriti")

# Caricamento dei dati
df = load_data()

if df.empty:
    st.warning("Non ci sono dati disponibili per generare grafici.")
else:
    # Creazione delle schede
    tabs = st.tabs([
        "Distribuzione Età",
        "Distribuzione Soddisfazione",
        "Fermi Totali",
        "Durata Media per Genere",
        "Hobby più Popolari",
        "Grafico Personalizzato"
    ])

    # Scheda 1: Distribuzione Età
    with tabs[0]:
        st.subheader("Distribuzione Età")
        fig = px.histogram(df, x="Età", nbins=10, title="Distribuzione delle Età")
        st.plotly_chart(fig, use_container_width=True)

    # Scheda 2: Distribuzione Soddisfazione
    with tabs[1]:
        st.subheader("Distribuzione Soddisfazione")
        fig = px.histogram(df, x="Soddisfazione", nbins=10, title="Livello di Soddisfazione")
        st.plotly_chart(fig, use_container_width=True)

    # Scheda 3: Fermi Totali
    with tabs[2]:
        st.subheader("Fermi Totali")
        df["Numero Fermi"] = df["Fermi"].apply(lambda x: len(x.split(" -- ")) if isinstance(x, str) else 0)
        fig = px.bar(df, x="Nome", y="Numero Fermi", title="Numero di Fermi per Utente")
        st.plotly_chart(fig, use_container_width=True)

    # Scheda 4: Durata Media per Genere
    with tabs[3]:
        st.subheader("Durata Media per Genere")
        df["Durata"] = pd.to_numeric(df["Durata"], errors="coerce").fillna(0)
        duration_by_genre = df.groupby("Genere")["Durata"].mean().reset_index()
        fig = px.bar(duration_by_genre, x="Genere", y="Durata", title="Durata Media per Genere")
        st.plotly_chart(fig, use_container_width=True)

    # Scheda 5: Hobby più Popolari
    with tabs[4]:
        st.subheader("Hobby più Popolari")
        hobby_list = df["Hobby"].dropna().str.split(" -- ").explode()
        hobby_count = hobby_list.value_counts().reset_index()
        hobby_count.columns = ["Hobby", "Frequenza"]
        fig = px.bar(hobby_count, x="Hobby", y="Frequenza", title="Hobby più Popolari")
        st.plotly_chart(fig, use_container_width=True)

    # Scheda 6: Grafico Personalizzato
    with tabs[5]:
        st.subheader("Grafico Personalizzato")
        columns = list(df.columns)
        x_axis = st.selectbox("Seleziona l'asse X", columns)
        y_axis = st.selectbox("Seleziona l'asse Y", columns)
        chart_type = st.selectbox("Seleziona il tipo di grafico", ["Bar", "Scatter", "Line"])

        if st.button("Genera Grafico"):
            if chart_type == "Bar":
                fig = px.bar(df, x=x_axis, y=y_axis, title=f"Grafico Bar: {x_axis} vs {y_axis}")
            elif chart_type == "Scatter":
                fig = px.scatter(df, x=x_axis, y=y_axis, title=f"Grafico Scatter: {x_axis} vs {y_axis}")
            elif chart_type == "Line":
                fig = px.line(df, x=x_axis, y=y_axis, title=f"Grafico Linea: {x_axis} vs {y_axis}")
            st.plotly_chart(fig, use_container_width=True)

