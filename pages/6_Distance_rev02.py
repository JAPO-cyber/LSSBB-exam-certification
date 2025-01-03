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

# Tab 11: Ricerca Aziende
st.header("Scheda 11: Ricerca Aziende")
if not api_key:
    st.warning("Inserisci la tua API Key per utilizzare la funzionalità.")
else:
    location = st.text_input("Inserisci la posizione di partenza (es. Via Roma, Milano)", "Via Roma, Milano")
    radius = st.slider("Seleziona il raggio di ricerca (in km)", min_value=1, max_value=100, value=10)
    keywords = st.text_input("Inserisci le attività da cercare separate da virgola", "elettricista, muratore, idraulico")
    max_results = st.number_input("Numero massimo di posizioni da cercare", min_value=1, max_value=100, value=20)

    if st.button("Cerca Aziende", key="search_businesses"):
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
                    # Prepara la ricerca
                    keyword_list = [kw.strip() for kw in keywords.split(",") if kw.strip()]
                    all_results = []

                    # Cerca per ogni parola chiave
                    for keyword in keyword_list:
                        next_page_token = None
                        results_count = 0

                        while results_count < max_results:
                            places_url = (
                                f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
                                f"location={lat},{lng}&radius={radius * 1000}&keyword={keyword}&key={api_key}"
                            )
                            if next_page_token:
                                places_url += f"&pagetoken={next_page_token}"

                            places_response = requests.get(places_url)
                            places_response.raise_for_status()
                            places_data = places_response.json()

                            if not places_data.get("results"):
                                break

                            for place in places_data["results"]:
                                if results_count >= max_results:
                                    break

                                place_name = place.get("name", "Senza Nome")
                                place_address = place.get("vicinity", "Indirizzo non disponibile")
                                place_location = place.get("geometry", {}).get("location", {})
                                lat_detail = place_location.get("lat")
                                lng_detail = place_location.get("lng")

                                # Ottieni dettagli aggiuntivi (numero di telefono, sito web, ecc.)
                                place_id = place.get("place_id")
                                types = ", ".join(place.get("types", []))  # Unisci i tipi in una stringa
                                phone_number = "Non disponibile"
                                international_phone_number = "Non disponibile"
                                website = "Non disponibile"

                                if place_id:
                                    details_url = (
                                        f"https://maps.googleapis.com/maps/api/place/details/json?"
                                        f"place_id={place_id}&fields=name,formatted_address,"
                                        f"formatted_phone_number,international_phone_number,website&key={api_key}"
                                    )
                                    details_response = requests.get(details_url)
                                    details_response.raise_for_status()
                                    details_data = details_response.json().get("result", {})
                                    phone_number = details_data.get("formatted_phone_number", "Non disponibile")
                                    international_phone_number = details_data.get("international_phone_number", "Non disponibile")
                                    website = details_data.get("website", "Non disponibile")

                                all_results.append({
                                    "Nome": place_name,
                                    "Indirizzo": place_address,
                                    "Telefono": phone_number,
                                    "Telefono Internazionale": international_phone_number,
                                    "Sito Web": website,
                                    "Types": types,  # Aggiungi il campo types
                                    "Latitudine": lat_detail,
                                    "Longitudine": lng_detail,
                                    "Keyword": keyword  # Traccia il tipo di attività
                                })

                                results_count += 1

                            next_page_token = places_data.get("next_page_token")
                            if not next_page_token:
                                break

                    if all_results:
                        df = pd.DataFrame(all_results)

                        # Salva i dati nel session state
                        st.session_state.df_data = df

                        # Crea la mappa
                        m = folium.Map(location=[lat, lng], zoom_start=12)
                        for _, row in df.iterrows():
                            folium.Marker(
                                location=[row["Latitudine"], row["Longitudine"]],
                                popup=f"{row['Nome']} ({row['Keyword']})\n{row['Indirizzo']}\n{row['Telefono']}",
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

# Mostra i risultati e la mappa
if st.session_state.df_data is not None:
    st.dataframe(st.session_state.df_data)

if st.session_state.map_data is not None:
    st_folium(st.session_state.map_data, width=700, height=500)


