import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# Configurazione dell'app
st.set_page_config(page_title="Google Maps API Demo", layout="wide")

# Header principale
st.title("Esempi di utilizzo delle Google Maps API")

# Input della chiave API
st.sidebar.header("Configurazione API")
api_key = st.sidebar.text_input("Inserisci la tua API Key", type="password")

# Controllo della chiave API
if not api_key:
    st.warning("Inserisci la tua API Key per utilizzare le funzionalità.")
else:
    # Tabs per gli esempi
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Calcolo Spese di Spedizione",
        "Ottimizzazione Percorsi",
        "Monitoraggio Tempo Reale",
        "Luoghi di Ritiro Vicini",
        "Geocoding Indirizzi"
    ])

    # Tab 1: Calcolo spese di spedizione
    with tab1:
        st.header("Calcolo Spese di Spedizione")
        origin = st.text_input("Indirizzo di partenza", "Via Roma, Milano")
        destination = st.text_input("Indirizzo di destinazione", "Piazza Duomo, Firenze")

        if st.button("Calcola Distanza"):
            url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={api_key}"
            response = requests.get(url).json()

            if response.get('rows'):
                distance = response['rows'][0]['elements'][0]['distance']['text']
                duration = response['rows'][0]['elements'][0]['duration']['text']
                st.success(f"Distanza: {distance}, Tempo stimato: {duration}")
            else:
                st.error("Errore nel calcolo della distanza.")

    # Tab 2: Ottimizzazione percorsi
    with tab2:
        st.header("Ottimizzazione Percorsi")
        origin = st.text_input("Punto di Partenza", "Via Venezia, Padova")
        destination = st.text_input("Destinazione Finale", "Via Napoli, Napoli")
        waypoints = st.text_input("Fermate Intermedie (separate da '|')", "Via Milano, Torino|Via Roma, Bologna")

        if st.button("Calcola Percorso"):
            url = (f"https://maps.googleapis.com/maps/api/directions/json?"
                   f"origin={origin}&destination={destination}&waypoints={waypoints}&key={api_key}")
            response = requests.get(url).json()

            if response.get('routes'):
                st.write("Percorso ottimale:")
                for leg in response['routes'][0]['legs']:
                    st.write(f"- Da {leg['start_address']} a {leg['end_address']}: {leg['distance']['text']}")
            else:
                st.error("Errore nel calcolo del percorso.")

    # Tab 3: Monitoraggio in tempo reale
    with tab3:
        st.header("Monitoraggio in Tempo Reale")
        locations = [(45.464211, 9.191383), (45.465422, 9.188553), (45.466533, 9.185723)]

        # Creazione mappa con Folium
        m = folium.Map(location=locations[0], zoom_start=15)
        for loc in locations:
            folium.Marker(location=loc, popup=f"Lat: {loc[0]}, Lon: {loc[1]}").add_to(m)

        st_folium(m, width=700, height=500)

    # Tab 4: Luoghi di ritiro vicini
    with tab4:
        st.header("Luoghi di Ritiro Vicini")
        location = st.text_input("Coordinate (latitudine, longitudine)", "45.464211,9.191383")
        radius = st.slider("Raggio di ricerca (metri)", 100, 5000, 1000)
        type_place = st.selectbox("Tipo di luogo", ["store", "restaurant", "gas_station"])

        if st.button("Cerca Luoghi"):
            url = (f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
                   f"location={location}&radius={radius}&type={type_place}&key={api_key}")
            response = requests.get(url).json()

            if response.get('results'):
                st.write("Luoghi trovati:")
                for place in response['results']:
                    name = place['name']
                    address = place.get('vicinity', 'Indirizzo non disponibile')
                    st.write(f"- {name}: {address}")
            else:
                st.error("Nessun luogo trovato.")

    # Tab 5: Geocoding indirizzi
    with tab5:
        st.header("Geocoding Indirizzi")
        address = st.text_input("Inserisci un indirizzo", "Piazza Duomo, Milano")

        if st.button("Ottieni Coordinate"):
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
            response = requests.get(url).json()

            if response.get('results'):
                location = response['results'][0]['geometry']['location']
                st.success(f"Coordinate: Latitudine {location['lat']}, Longitudine {location['lng']}")
            else:
                st.error("Errore nella geocodifica.")
