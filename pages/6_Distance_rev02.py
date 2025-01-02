import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# Configurazione dell'app
st.set_page_config(page_title="Route Optimization Demo", layout="wide")

# Header principale
st.title("Route Optimization con OR-Tools e Google Maps API")

# Input della chiave API
st.sidebar.header("Configurazione API")
api_key = st.sidebar.text_input("Inserisci la tua API Key", type="password")

# Tab 11: Ricerca Aziende di Elettricisti
st.header("Scheda 11: Ricerca Aziende di Elettricisti")
if not api_key:
    st.warning("Inserisci la tua API Key per utilizzare la funzionalità.")
else:
    location = st.text_input("Inserisci la posizione di partenza (es. Via Roma, Milano)", "Via Roma, Milano")
    radius = st.slider("Seleziona il raggio di ricerca (in km)", min_value=1, max_value=100, value=10)
    keyword = "elettricisti"

    if st.button("Cerca Aziende", key="search_electricians"):
        try:
            # Ottieni le coordinate della posizione di partenza
            geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
            geocode_response = requests.get(geocode_url)
            geocode_response.raise_for_status()
            geocode_data = geocode_response.json()

            # Log per il debug
            st.write("Risultato Geocoding API:", geocode_data)

            if not geocode_data.get("results"):
                st.error("Errore: Impossibile trovare le coordinate della posizione di partenza. Verifica l'indirizzo inserito.")
            else:
                coordinates = geocode_data["results"][0]["geometry"]["location"]
                lat, lng = coordinates["lat"], coordinates["lng"]

                # Effettua la ricerca di aziende tramite Places API
                places_url = (
                    f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
                    f"location={lat},{lng}&radius={radius * 1000}&keyword={keyword}&key={api_key}"
                )
                places_response = requests.get(places_url)
                places_response.raise_for_status()
                places_data = places_response.json()

                # Log per il debug
                st.write("Risultato Places API:", places_data)

                if not places_data.get("results"):
                    st.warning("Nessuna azienda trovata nel raggio selezionato.")
                else:
                    st.success(f"Trovate {len(places_data['results'])} aziende di elettricisti.")

                    # Mostra i risultati in una lista e su una mappa
                    m = folium.Map(location=[lat, lng], zoom_start=12)
                    for place in places_data["results"]:
                        place_name = place.get("name", "Senza Nome")
                        place_address = place.get("vicinity", "Indirizzo non disponibile")
                        place_location = place["geometry"]["location"]
                        folium.Marker(
                            location=[place_location["lat"], place_location["lng"]],
                            popup=f"{place_name}\n{place_address}",
                            icon=folium.Icon(color="blue", icon="info-sign")
                        ).add_to(m)
                        st.write(f"- **{place_name}**: {place_address}")

                    st_folium(m, width=700, height=500)
        except requests.exceptions.RequestException as e:
            st.error(f"Errore durante la richiesta API: {e}")
        except Exception as e:
            st.error(f"Errore durante l'elaborazione: {e}")


