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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
        "Calcolo Spese di Spedizione",
        "Ottimizzazione Percorsi",
        "Monitoraggio Tempo Reale",
        "Luoghi di Ritiro Vicini",
        "Geocoding Indirizzi",
        "Traffico in Tempo Reale",
        "Multi-Consegne",
        "Monitoraggio Parco Veicoli",
        "Tempi di Consegna Multipli",
        "Ottimizzazione del Carico",
        "Percorso su Mappa"
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

    # Tab 2: Ottimizzazione percorsi
    with tab2:
        st.header("Ottimizzazione Percorsi")
        origin = st.text_input("Punto di Partenza", "Via Venezia, Padova")
        destination = st.text_input("Destinazione Finale", "Via Napoli, Napoli")
        waypoints = st.text_input("Fermate Intermedie (separate da '|')", "Via Milano, Torino|Via Roma, Bologna")

        if st.button("Calcola Percorso", key="tab2"):
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

        if st.button("Cerca Luoghi", key="tab4"):
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

        if st.button("Ottieni Coordinate", key="tab5"):
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
            response = requests.get(url).json()

            if response.get('results'):
                location = response['results'][0]['geometry']['location']
                st.success(f"Coordinate: Latitudine {location['lat']}, Longitudine {location['lng']}")
            else:
                st.error("Errore nella geocodifica.")

    # Tab 6: Stima del traffico in tempo reale
    with tab6:
        st.header("Stima del Tempo con Traffico")
        origin = st.text_input("Punto di partenza", "Via Roma, Milano")
        destination = st.text_input("Destinazione", "Piazza Duomo, Firenze")

        if st.button("Calcola Tempo con Traffico", key="tab6"):
            url = (f"https://maps.googleapis.com/maps/api/directions/json?"
                   f"origin={origin}&destination={destination}&departure_time=now&key={api_key}")
            response = requests.get(url).json()

            if response.get('routes'):
                duration_in_traffic = response['routes'][0]['legs'][0]['duration_in_traffic']['text']
                st.success(f"Tempo stimato considerando il traffico: {duration_in_traffic}")
            else:
                st.error("Errore nel calcolo del tempo con traffico.")

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

    # Tab 10: Pianificazione del Carico
    with tab10:
        st.header("Pianificazione del Carico")
        carico_max = st.number_input("Capacità massima del veicolo (kg)", min_value=1, value=1000, key="tab10_carico_max")
        ordini = st.text_area(
            "Inserisci gli ordini (formato: Indirizzo, Peso in kg per riga)",
            "Via Roma, Milano, 300\nPiazza Duomo, Firenze, 500\nVia Napoli, Napoli, 200",
            key="tab10_ordini"
        )

        if st.button("Pianifica Carico", key="tab10"):
            ordini_list = [
                line.split(", ") for line in ordini.strip().split("\n")
            ]
            totale_peso = sum(int(ordine[2]) for ordine in ordini_list)
            if totale_peso > carico_max:
                st.warning(f"Il carico totale ({totale_peso} kg) supera la capacità del veicolo ({carico_max} kg).")
            else:
                st.success("Il carico totale rientra nei limiti!")
                for ordine in ordini_list:
                    st.write(f"- {ordine[0]}: {ordine[2]} kg")
                    
    # Tab 11: Percorso su mappa
    with tab11:
        st.header("Movimentazione del Mezzo su Mappa")
    
        # Input per inserire una serie di indirizzi
        addresses_input = st.text_area(
            "Inserisci gli indirizzi separati da una nuova riga:",
            placeholder="Indirizzo 1\nIndirizzo 2\nIndirizzo 3",
        )
    
        if st.button("Mostra Movimentazione", key="show_route"):
            # Suddividi gli indirizzi in una lista, ignorando righe vuote
            addresses = [address.strip() for address in addresses_input.split("\n") if address.strip()]
    
            if not addresses:
                st.error("Inserisci almeno un indirizzo valido.")
            else:
                # Geocodifica gli indirizzi con Google Maps API
                api_key = st.secrets["google_api"]["api_key"]  # Assicurati di aver configurato st.secrets
                locations = []
    
                for address in addresses:
                    try:
                        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
                        response = requests.get(geocode_url)
                        response.raise_for_status()
                        geocode_data = response.json()
    
                        if geocode_data["status"] == "OK":
                            location = geocode_data["results"][0]["geometry"]["location"]
                            locations.append((location["lat"], location["lng"]))
                        else:
                            st.warning(f"Indirizzo non trovato o errore: {address}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Errore durante la richiesta API: {e}")
    
                if not locations:
                    st.error("Nessuna posizione valida trovata.")
                else:
                    # Creazione della mappa
                    start_location = locations[0]  # Punto di partenza
                    route_map = folium.Map(location=start_location, zoom_start=13)
    
                    # Aggiungi i marker e la rotta
                    for i, coord in enumerate(locations):
                        folium.Marker(
                            location=coord,
                            popup=f"Step {i + 1}: {addresses[i]}",
                            icon=folium.Icon(color="blue", icon="info-sign"),
                        ).add_to(route_map)
    
                    # Disegna la rotta
                    folium.PolyLine(locations, color="blue", weight=2.5, opacity=1).add_to(route_map)
    
                    # Mostra la mappa
                    st_folium(route_map, width=800, height=600)
