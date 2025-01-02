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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "Calcolo Spese di Spedizione",
        "Ottimizzazione Percorsi",
        "Monitoraggio Tempo Reale",
        "Luoghi di Ritiro Vicini",
        "Geocoding Indirizzi",
        "Traffico in Tempo Reale",
        "Multi-Consegne",
        "Monitoraggio Parco Veicoli",
        "Tempi di Consegna Multipli",
        "Ottimizzazione del Carico"
    ])

    # Tab 1: Calcolo spese di spedizione
    with tab1:
        st.header("Calcolo Spese di Spedizione")
        origin = st.text_input("Indirizzo di partenza", "Via Roma, Milano")
        destination = st.text_input("Indirizzo di destinazione", "Piazza Duomo, Firenze")

        if st.button("Calcola Distanza", key="tab1"):
            url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={api_key}"
            response = requests.get(url).json()

            if response.get('rows'):
                distance = response['rows'][0]['elements'][0]['distance']['text']
                duration = response['rows'][0]['elements'][0]['duration']['text']
                st.success(f"Distanza: {distance}, Tempo stimato: {duration}")
            else:
                st.error("Errore nel calcolo della distanza.")

    # Tab 7: Multi-Consegne
    with tab7:
        st.header("Pianificazione Multi-Consegne")
        origins = st.text_input("Indirizzi di partenza (separati da '|')", "Via Roma, Milano|Via Torino, Torino")
        destinations = st.text_input("Indirizzi di destinazione (separati da '|')", "Piazza Duomo, Firenze|Via Napoli, Napoli")

        if st.button("Calcola Distanze", key="tab7"):
            url = (f"https://maps.googleapis.com/maps/api/distancematrix/json?"
                   f"origins={origins}&destinations={destinations}&key={api_key}")
            response = requests.get(url).json()

            if response.get('rows'):
                st.write("Distanze calcolate:")
                for i, row in enumerate(response['rows']):
                    for j, element in enumerate(row['elements']):
                        origin = origins.split('|')[i]
                        destination = destinations.split('|')[j]
                        st.write(f"- Da {origin} a {destination}: {element['distance']['text']}, {element['duration']['text']}")
            else:
                st.error("Errore nel calcolo delle distanze.")

    # Tab 8: Monitoraggio Parco Veicoli
    with tab8:
        st.header("Monitoraggio Parco Veicoli")
        vehicle_locations = [
            {"name": "Camion 1", "lat": 45.464211, "lon": 9.191383},
            {"name": "Camion 2", "lat": 45.465422, "lon": 9.188553},
            {"name": "Camion 3", "lat": 45.466533, "lon": 9.185723},
        ]

        # Creazione mappa con Folium
        m = folium.Map(location=[45.464211, 9.191383], zoom_start=13)
        for vehicle in vehicle_locations:
            folium.Marker(
                location=[vehicle["lat"], vehicle["lon"]],
                popup=f"{vehicle['name']}",
                icon=folium.Icon(color="blue")
            ).add_to(m)

        st_folium(m, width=700, height=500)

    # Tab 9: Tempi di Consegna Multipli
    with tab9:
        st.header("Tempi di Consegna Multipli")
        warehouse = st.text_input("Indirizzo del magazzino", "Via Roma, Milano", key="warehouse_tab9")
        customers = st.text_input("Indirizzi dei clienti (separati da '|')", "Piazza Duomo, Firenze|Via Napoli, Napoli", key="customers_tab9")

        if st.button("Calcola Tempi di Consegna", key="tab9"):
            url = (f"https://maps.googleapis.com/maps/api/distancematrix/json?"
                   f"origins={warehouse}&destinations={customers}&key={api_key}")
            response = requests.get(url).json()

            if response.get('rows') and response['rows'][0]['elements']:
                st.write("Tempi di consegna stimati:")
                for i, element in enumerate(response['rows'][0]['elements']):
                    destination = customers.split('|')[i]
                    if element['status'] == "OK":
                        st.write(f"- A {destination}: {element['duration']['text']}")
                    else:
                        st.warning(f"- A {destination}: Nessuna stima disponibile")
            else:
                st.error("Errore nel calcolo dei tempi di consegna.")

    # Tab 10: Ottimizzazione del Carico
    with tab10:
        st.header("Ottimizzazione del Carico")
        addresses = st.text_area("Inserisci gli indirizzi (uno per riga)", "Via Roma, Milano\nPiazza Duomo, Firenze\nVia Napoli, Napoli", key="addresses_tab10")

        if st.button("Ottimizza Ordine di Consegna", key="tab10"):
            addresses_list = addresses.split("\n")
            if len(addresses_list) < 2:
                st.warning("Inserisci almeno due indirizzi per l'ottimizzazione.")
            else:
                # Calcolo della Distance Matrix per tutti i punti
                origins = "|".join(addresses_list)
                destinations = "|".join(addresses_list)

                url = (f"https://maps.googleapis.com/maps/api/distancematrix/json?"
                       f"origins={origins}&destinations={destinations}&key={api_key}")
                response = requests.get(url).json()

                if response.get('rows'):
                    st.write("Ordine di consegna ottimizzato (approssimativo):")
                    visited = [addresses_list[0]]  # Partenza dal primo indirizzo
                    to_visit = set(addresses_list[1:])

                    while to_visit:
                        current = visited[-1]
                        distances = {}
                        for destination in to_visit:
                            origin_idx = addresses_list.index(current)
                            dest_idx = addresses_list.index(destination)
                            element = response['rows'][origin_idx]['elements'][dest_idx]
                            if element['status'] == "OK":
                                distances[destination] = element['distance']['value']  # Distanza in metri
                        # Trova il più vicino
                        next_stop = min(distances, key=distances.get)
                        visited.append(next_stop)
                        to_visit.remove(next_stop)

                    for address in visited:
                        st.write(f"- {address}")
                else:
                    st.error("Errore nel calcolo della matrice di distanze.")

