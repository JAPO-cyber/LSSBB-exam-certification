import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from shapely.geometry import Point, Polygon

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
    # Scelta della funzionalità
    funzionalita = st.selectbox(
        "Scegli una funzionalità",
        [
            "Calcolo del Costo di Consegna e CO₂",
            "Zone di Consegna Intelligenti",
            "Ottimizzazione Multi-Consegna",
            "Pianificazione del Carico"
        ]
    )

    # **1. Calcolo del Costo di Consegna e CO₂**
    if funzionalita == "Calcolo del Costo di Consegna e CO₂":
        st.header("Calcolo del Costo di Consegna e CO₂")
        origin = st.text_input("Indirizzo di partenza", "Via Roma, Milano")
        destination = st.text_input("Indirizzo di destinazione", "Piazza Duomo, Firenze")
        costo_per_km = st.number_input("Costo per km (€)", min_value=0.0, value=0.5, step=0.1)
        emissioni_co2_per_km = st.number_input("Emissioni di CO₂ per km (g)", min_value=0.0, value=120.0, step=1.0)

        if st.button("Calcola"):
            url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={api_key}"
            response = requests.get(url).json()

            if response.get('rows'):
                distanza = response['rows'][0]['elements'][0]['distance']['value'] / 1000  # Converti in km
                costo_totale = distanza * costo_per_km
                emissioni_totali = distanza * emissioni_co2_per_km
                st.success(f"Distanza: {distanza:.2f} km")
                st.info(f"Costo totale: €{costo_totale:.2f}")
                st.info(f"Emissioni di CO₂: {emissioni_totali:.2f} g")
            else:
                st.error("Errore nel calcolo della distanza.")

    # **2. Zone di Consegna Intelligenti**
    elif funzionalita == "Zone di Consegna Intelligenti":
        st.header("Zone di Consegna Intelligenti")
        address = st.text_input("Indirizzo da verificare", "Piazza Duomo, Milano")
        zona = st.text_area(
            "Coordinate della zona (latitudine, longitudine per riga)",
            "45.464211, 9.191383\n45.466533, 9.185723\n45.465422, 9.188553"
        )

        if st.button("Verifica Zona"):
            # Ottieni coordinate dell'indirizzo
            geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
            geocode_response = requests.get(geocode_url).json()
            if geocode_response.get("results"):
                location = geocode_response["results"][0]["geometry"]["location"]
                point = Point(location["lat"], location["lng"])
                
                # Crea poligono della zona
                zona_coords = [
                    tuple(map(float, line.split(", ")))
                    for line in zona.strip().split("\n")
                ]
                polygon = Polygon(zona_coords)

                # Verifica se il punto è nella zona
                if polygon.contains(point):
                    st.success("L'indirizzo si trova nella zona definita.")
                else:
                    st.error("L'indirizzo non si trova nella zona definita.")
            else:
                st.error("Errore nel calcolo delle coordinate dell'indirizzo.")

    # **3. Ottimizzazione Multi-Consegna**
    elif funzionalita == "Ottimizzazione Multi-Consegna":
        st.header("Ottimizzazione Multi-Consegna")
        addresses = st.text_area("Inserisci gli indirizzi (uno per riga)", "Via Roma, Milano\nPiazza Duomo, Firenze\nVia Napoli, Napoli")

        if st.button("Ottimizza Percorso"):
            addresses_list = addresses.split("\n")
            origins = "|".join(addresses_list)
            destinations = "|".join(addresses_list)

            url = (f"https://maps.googleapis.com/maps/api/distancematrix/json?"
                   f"origins={origins}&destinations={destinations}&key={api_key}")
            response = requests.get(url).json()

            if response.get('rows'):
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
                            distances[destination] = element['distance']['value']
                    # Trova il più vicino
                    next_stop = min(distances, key=distances.get)
                    visited.append(next_stop)
                    to_visit.remove(next_stop)

                st.write("Ordine ottimizzato:")
                for address in visited:
                    st.write(f"- {address}")
            else:
                st.error("Errore nel calcolo della matrice di distanze.")

    # **4. Pianificazione del Carico**
    elif funzionalita == "Pianificazione del Carico":
        st.header("Pianificazione del Carico")
        carico_max = st.number_input("Capacità massima del veicolo (kg)", min_value=1, value=1000)
        ordini = st.text_area(
            "Inserisci gli ordini (formato: Indirizzo, Peso in kg per riga)",
            "Via Roma, Milano, 300\nPiazza Duomo, Firenze, 500\nVia Napoli, Napoli, 200"
        )

        if st.button("Pianifica Carico"):
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


