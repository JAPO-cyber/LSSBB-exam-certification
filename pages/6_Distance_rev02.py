import streamlit as st
import requests
import folium
import pandas as pd
from streamlit_folium import st_folium

# Configurazione dell'app
st.set_page_config(page_title="Route Optimization Demo", layout="wide")

# Header principale
st.title("Route Optimization con OR-Tools e Google Maps API")

# Input della chiave API
st.sidebar.header("Configurazione API")
api_key = st.sidebar.text_input("Inserisci la tua API Key", type="password")

# Variabile di stato per la mappa e i risultati
if "map_data" not in st.session_state:
    st.session_state.map_data = None
if "df_data" not in st.session_state:
    st.session_state.df_data = None

# Tab 11: Ricerca Aziende di Elettricisti
st.header("Scheda 11: Ricerca Aziende")
if not api_key:
    st.warning("Inserisci la tua API Key per utilizzare la funzionalità.")
else:
    location = st.text_input("Inserisci la posizione di partenza (es. Via Roma, Milano)", "Via Roma, Milano")
    radius = st.slider("Seleziona il raggio di ricerca (in km)", min_value=1, max_value=100, value=10)
    keyword = st.text_input("Inserisci il tipo di attività da cercare", "elettricisti")

    if st.button("Cerca Aziende", key="search_electricians"):
        try:
            # Ottieni le coordinate della posizione di partenza
            geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
            geocode_response = requests.get(geocode_url)
            geocode_response.raise_for_status()
            geocode_data = geocode_response.json()

            if not geocode_data.get("results"):
                st.error("Errore: Impossibile trovare le coordinate della posizione di partenza.")
            else:
                coordinates = geocode_data["results"][0]["geometry"]["location"]
                lat = coordinates.get("lat")
                lng = coordinates.get("lng")

                if lat is None or lng is None:
                    st.error("Errore: Le coordinate della posizione non sono valide.")
                else:
                    # Effettua la ricerca di aziende tramite Places API
                    places_url = (
                        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
                        f"location={lat},{lng}&radius={radius * 1000}&keyword={keyword}&key={api_key}"
                    )
                    places_response = requests.get(places_url)
                    places_response.raise_for_status()
                    places_data = places_response.json()

                    if not places_data.get("results"):
                        st.warning("Nessuna azienda trovata nel raggio selezionato.")
                    else:
                        st.success(f"Trovate {len(places_data['results'])} aziende per '{keyword}'.")

                        # Creazione di un DataFrame per i risultati
                        results = []
                        for place in places_data["results"]:
                            place_name = place.get("name", "Senza Nome")
                            place_address = place.get("vicinity", "Indirizzo non disponibile")
                            place_location = place.get("geometry", {}).get("location", {})
                            lat_detail = place_location.get("lat")
                            lng_detail = place_location.get("lng")

                            if lat_detail is not None and lng_detail is not None:
                                results.append({
                                    "Nome": place_name,
                                    "Indirizzo": place_address,
                                    "Latitudine": lat_detail,
                                    "Longitudine": lng_detail
                                })

                        if results:
                            df = pd.DataFrame(results)

                            # Salva i dati nel session state
                            st.session_state.df_data = df

                            # Crea la mappa
                            m = folium.Map(location=[lat, lng], zoom_start=12)
                            for _, row in df.iterrows():
                                folium.Marker(
                                    location=[row["Latitudine"], row["Longitudine"]],
                                    popup=f"{row['Nome']}\n{row['Indirizzo']}",
                                    icon=folium.Icon(color="blue", icon="info-sign")
                                ).add_to(m)

                            # Salva la mappa nel session state
                            st.session_state.map_data = m
                        else:
                            st.warning("Non è stato possibile recuperare dettagli validi per le aziende trovate.")

        except requests.exceptions.RequestException as e:
            st.error(f"Errore durante la richiesta API: {e}")
        except Exception as e:
            st.error(f"Errore durante l'elaborazione: {e}")

# Mostra i risultati salvati nel session state
if st.session_state.df_data is not None:
    st.dataframe(st.session_state.df_data)

if st.session_state.map_data is not None:
    st_folium(st.session_state.map_data, width=700, height=500)


