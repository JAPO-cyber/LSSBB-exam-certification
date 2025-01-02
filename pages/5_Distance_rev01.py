import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# Configurazione dell'app
st.set_page_config(page_title="Route Optimization Demo", layout="wide")

# Header principale
st.title("Route Optimization con OR-Tools e Google Maps API")

# Input della chiave API
st.sidebar.header("Configurazione API")
api_key = st.sidebar.text_input("Inserisci la tua API Key", type="password")

# Controllo della chiave API
if not api_key:
    st.warning("Inserisci la tua API Key per utilizzare la funzionalità.")
else:
    st.header("Ottimizzazione del Percorso")
    addresses = st.text_area(
        "Inserisci gli indirizzi (uno per riga)",
        "Via Roma, Milano\nPiazza Duomo, Firenze\nVia Napoli, Napoli",
        key="route_optimization_addresses"
    )

    if st.button("Ottimizza Percorso", key="route_optimization"):
        addresses_list = addresses.split("\n")
        if len(addresses_list) < 2:
            st.warning("Inserisci almeno due indirizzi.")
        else:
            # Step 1: Calcolo della matrice di distanze
            try:
                origins = "|".join(addresses_list)
                destinations = "|".join(addresses_list)
                url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={destinations}&key={api_key}"
                response = requests.get(url)
                response.raise_for_status()  # Solleva un errore se la richiesta non è andata a buon fine
                response_data = response.json()

                if response_data.get('rows'):
                    # Costruzione della matrice di distanze
                    distance_matrix = []
                    for row in response_data['rows']:
                        distances = [
                            element.get('distance', {}).get('value', float('inf'))
                            for element in row['elements']
                        ]
                        distance_matrix.append(distances)

                    st.write("Matrice di distanze calcolata con successo:")
                    st.json(distance_matrix)

                    # Step 2: Configurazione del problema di ottimizzazione
                    def create_data_model():
                        """Crea il modello di dati per il problema."""
                        data = {
                            'distance_matrix': distance_matrix,
                            'num_vehicles': 1,
                            'depot': 0
                        }
                        return data

                    data = create_data_model()

                    # Creazione del gestore dati
                    manager = pywrapcp.RoutingIndexManager(
                        len(data['distance_matrix']),
                        data['num_vehicles'],
                        data['depot']
                    )

                    # Creazione del modello di routing
                    routing = pywrapcp.RoutingModel(manager)

                    # Definizione della funzione di costo
                    def distance_callback(from_index, to_index):
                        """Restituisce la distanza tra due nodi."""
                        from_node = manager.IndexToNode(from_index)
                        to_node = manager.IndexToNode(to_index)
                        return data['distance_matrix'][from_node][to_node]

                    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
                    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

                    # Configurazione della ricerca
                    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
                    search_parameters.first_solution_strategy = (
                        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
                    )

                    # Risoluzione del problema
                    solution = routing.SolveWithParameters(search_parameters)

                    # Estrazione del percorso
                    if solution:
                        route = []
                        index = routing.Start(0)
                        while not routing.IsEnd(index):
                            route.append(manager.IndexToNode(index))
                            index = solution.Value(routing.NextVar(index))
                        route.append(manager.IndexToNode(index))

                        # Mostra il percorso ottimizzato
                        st.write("Percorso ottimizzato:")
                        for idx in route:
                            st.write(f"- {addresses_list[idx]}")

                        # Visualizzazione su mappa con persistenza
                        try:
                            waypoints = "|".join([addresses_list[idx] for idx in route[1:-1]])
                            url_directions = (f"https://maps.googleapis.com/maps/api/directions/json?"
                                              f"origin={addresses_list[route[0]]}&destination={addresses_list[route[-1]]}"
                                              f"&waypoints={waypoints}&key={api_key}")
                            response_directions = requests.get(url_directions)
                            response_directions.raise_for_status()
                            route_data = response_directions.json()

                            if route_data.get('routes'):
                                route_info = route_data['routes'][0]
                                m = folium.Map(location=[
                                    route_info['legs'][0]['start_location']['lat'],
                                    route_info['legs'][0]['start_location']['lng']
                                ], zoom_start=6)

                                # Aggiunta della polilinea
                                folium.PolyLine(
                                    locations=[
                                        [step['start_location']['lat'], step['start_location']['lng']]
                                        for leg in route_info['legs']
                                        for step in leg['steps']
                                    ],
                                    color="blue",
                                    weight=5,
                                    opacity=0.7
                                ).add_to(m)

                                # Aggiunta dei marker per le destinazioni
                                for idx, leg in enumerate(route_info['legs']):
                                    if idx + 1 < len(addresses_list):
                                        folium.Marker(
                                            location=[leg['end_location']['lat'], leg['end_location']['lng']],
                                            popup=f"Fermata {idx + 1}: {addresses_list[idx + 1]}",
                                            icon=folium.Icon(color="green" if idx == len(route_info['legs']) - 1 else "red")
                                        ).add_to(m)

                                st_folium(m, width=700, height=500)
                            else:
                                st.error("Errore nella visualizzazione del percorso.")
                        except Exception as e:
                            st.error(f"Errore nella visualizzazione del percorso: {e}")
                    else:
                        st.error("Errore nell'ottimizzazione del percorso.")
                else:
                    st.error("Errore nel calcolo della matrice di distanze.")

            except requests.exceptions.RequestException as e:
                st.error(f"Errore durante la richiesta API: {e}")
            except Exception as e:
                st.error(f"Errore durante l'elaborazione: {e}")


