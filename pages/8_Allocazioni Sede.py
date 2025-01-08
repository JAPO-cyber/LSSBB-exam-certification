import streamlit as st
import pandas as pd
import io

# Definizione del codice 
# Configurazione dell'analisi

def calculate_scenario_values(Original_Road, Province, Configurazione_sedi):

    Original_Road["Provincia Partenza"]=Original_Road["Provincia_Partenza_Corretta"]
    Original_Road["Provincia Arrivo"]=Original_Road["Sede_arrivo_corretta"]
    Original_Road["Tipologia Servizio"]=Original_Road["Tipologia Contratto"]

    # Scelgo sono le configurazioni univoche per la simulazione [la scelta di sviluppo è legata alla velocità del codice (30 secondi vs 30 minuti)]
    Road= Original_Road[['Provincia Partenza', 'Provincia Arrivo','Tipologia Servizio']].copy()
    #Road = Road[(Road["Provincia Partenza"]=='BG') & (Road["Provincia Arrivo"]=='VE') & (Road["Tipologia Servizio"]=="Rent")]
    Road=Road.drop_duplicates()
    Road.head(5)

    Province['Path']=Province['Provincia Origine'].astype(str)+'-'+Province['Provincia Arrivo'].astype(str)

    #Configuro il file di output
    Road['Path_originale']=Road['Provincia Partenza'].astype(str)+'-'+Road['Provincia Arrivo'].astype(str)
    Road['Distanza Baseline']=None
    Road['Tempo Baseline']=None

    # Configuro i vari scenari
    for colonna in Configurazione_sedi.columns[1:]:
        nome_colonna=colonna
        # Creo le colonne per il calcolo dello scenario
        colonna1=colonna+'- Distanza Km'
        colonna2=colonna+'- Tempo '
        colonna3=colonna+'- Sede Riferimento'
        Road[colonna1]=None
        Road[colonna2]=None
        Road[colonna3]=None


    for index,row in Road.iterrows():
        # Percorso originale partenza- arrivo
        valore_cercato=row['Path_originale']
        if valore_cercato in Province['Path'].values:
            Road.at[index,'Distanza Baseline']=Province.loc[Province['Path']==valore_cercato,'Distanza km'].values[0]
            Road.at[index,'Tempo Baseline']=Province.loc[Province['Path']==valore_cercato,'Durata minuti'].values[0]
        else:
            Road.at[index,'Distanza Baseline']= None
            Road.at[index,'Tempo Baseline']=None
        
        # Configuro i dati di gestione
        arrivo=row['Provincia Arrivo']
        tipo_servizio=row['Tipologia Servizio']


        # Calcolo i valori dello scenario di riferimento
        for colonna in Configurazione_sedi.columns[1:]:
            nome_colonna=colonna
            # Definisco le colonne di salvataggio
            colonna1=colonna+'- Distanza Km'
            colonna2=colonna+'- Tempo '
            colonna3=colonna+'- Sede Riferimento'
            # Definisco il dataframe per la gestione della colonna
            colonna_dataframe=pd.DataFrame(columns=['sede','tipo sede','km','tempo'])

            #Utilizzo solo le colonne non nulle
            non_null_count=Configurazione_sedi[colonna].count()

            try:
                # Vincolo sulla partenza
                if non_null_count>0:
                    #Creo la lista di calcolo
                    for index_1,row_1 in Configurazione_sedi.iterrows():
                        value=row_1[colonna] #Recupero la lettera della sede
                        try:
                            valore_corrispondente=row_1[Configurazione_sedi.columns[0]] #Recupero ad esempio Bergamo
                            concatenato=valore_corrispondente+'-'+arrivo # Crea la nuova coppia
                        except:
                            concatenato='errore'
                            
                        if concatenato in Province['Path'].values:
                            # Trovo il valore corrispondente nella tabella
                            colonna_dataframe.at[index_1,'sede']=valore_corrispondente
                            colonna_dataframe.at[index_1,'tipo sede']=value
                            try:
                                colonna_dataframe.at[index_1,'km']=Province.loc[Province['Path']==concatenato,'Distanza km'].values[0]
                                colonna_dataframe.at[index_1,'tempo']=Province.loc[Province['Path']==concatenato,'Durata minuti'].values[0]
                            except:
                                colonna_dataframe.at[index_1,'km']=0
                                colonna_dataframe.at[index_1,'tempo']=0

                    # Filtro il dataframe per delle condizioni sfruttando un case when
                    if tipo_servizio=='Trade':
                        #filtro il dataframe con la condizione A
                        colonna_dataframe_filtered=colonna_dataframe[colonna_dataframe['tipo sede']=='A']
                        try:
                            min_km_row=colonna_dataframe_filtered.loc[colonna_dataframe_filtered['km'].idxmin()]
                            Road.at[index,colonna3]=min_km_row['sede']
                            Road.at[index,colonna1]=min_km_row['km']
                            Road.at[index,colonna2]=min_km_row['tempo']
                        except ValueError as e:
                            e=1
                            #print(arrivo)

                    else:    
                        colonna_dataframe_filtered=colonna_dataframe[(colonna_dataframe['tipo sede']=='A') | (colonna_dataframe['tipo sede']=='B')]
                        try:
                            print(colonna_dataframe_filtered)
                            min_km_row=colonna_dataframe_filtered.loc[colonna_dataframe_filtered['km'].idxmin()]
                            Road.at[index,colonna3]=min_km_row['sede']
                            Road.at[index,colonna1]=min_km_row['km']
                            Road.at[index,colonna2]=min_km_row['tempo']
                            print(min_km_row['sede'])
                        except ValueError as e:
                            e=1
                            #print(e)
                            #print(arrivo)
            except ValueError as e:
                print(e)       

    Road_filtered = Road[
    (Road["Provincia Partenza"].notna()) & (Road["Provincia Partenza"] != "") & (Road["Provincia Partenza"] != 0) &
    (Road["Provincia Arrivo"].notna()) & (Road["Provincia Arrivo"] != "") & (Road["Provincia Arrivo"] != 0) &
    (Road["Distanza Baseline"].notna()) & (Road["Distanza Baseline"] != "") & (Road["Distanza Baseline"] != 0) ]
    
    return Road_filtered



# Configurazione della pagina
st.set_page_config(page_title="Analisi Logistica", layout="wide")

# Variabili di stato
if "road_data" not in st.session_state:
    st.session_state.road_data = None

if "calculated" not in st.session_state:
    st.session_state.calculated = False

if "allocation_started" not in st.session_state:
    st.session_state.allocation_started = False

# Tabs principali
tab1, tab2 = st.tabs(["📂 Caricamento File", "📊 Risultati Analisi"])

# Tab 1: Caricamento File
with tab1:
    st.header("Caricamento e Modifica File")

    # Caricamento dei file
    st.sidebar.header("Caricamento File")
    file1 = st.sidebar.file_uploader("Carica il file 'GS_KAR_DB_Completo.xlsx'", type=["xlsx"])
    file2 = st.sidebar.file_uploader("Carica il file 'Configurazione_sedi.xlsx'", type=["xlsx"])
    file3 = st.sidebar.file_uploader("Carica il file 'Distanze_province.xlsx'", type=["xlsx"])

    if file1 and file2 and file3:
        try:
            # Lettura file caricati
            st.subheader("Visualizzazione Dati")
            
            # File 1: GS_KAR_DB_Completo.xlsx
            st.write("### File 1: GS_KAR_DB_Completo")
            Original_Road = pd.read_excel(file1, sheet_name='Foglio1')
            st.dataframe(Original_Road.head(10))
            
            # File 2: Configurazione_sedi.xlsx
            st.write("### File 2: Configurazione Sedi - Modifica Interattiva")
            Configurazione_sedi = pd.read_excel(file2, sheet_name='Configurazione_scenari')
            edited_sedi = st.data_editor(Configurazione_sedi, use_container_width=True, num_rows="dynamic")
            
            # File 3: Distanze_province.xlsx
            st.write("### File 3: Distanze Province")
            Province = pd.read_excel(file3, sheet_name='distanze revised')
            st.dataframe(Province.head(10))
                                    
            # Salva i dati nella sessione
            st.session_state.road_data = Original_Road
            st.session_state.sedi_data = edited_sedi
            st.session_state.province_data = Province
            
        except Exception as e:
            st.error(f"Errore durante l'elaborazione: {e}")
    else:
        st.warning("Carica tutti i file richiesti per continuare.")

# Tab 2: Risultati Analisi
with tab2:
    st.header("Risultati Analisi")

    if st.session_state.road_data is not None:
        if st.button("Avvia Allocazione"):
            st.session_state.allocation_started = True
            st.success("Codice di allocazione avviato!")

        if st.session_state.allocation_started:
            if not st.session_state.calculated:
                if st.button("Calcola Allocazione"):
                     st.session_state.road_data = calculate_scenario_values(st.session_state.road_data, st.session_state.province_data, st.session_state.sedi_data)
                     st.session_state.calculated = True
            if st.session_state.calculated:
                st.write("### Tabella con Risultati")
                st.dataframe(st.session_state.road_data.head(10))

                # Scaricamento dei risultati
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    st.session_state.road_data.to_excel(writer, index=False, sheet_name='Risultati')
                st.download_button(
                    label="Scarica Risultati in Excel",
                    data=output.getvalue(),
                    file_name="Output_Analisi.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
    else:
        st.warning("Carica i file nella prima tab e premi il pulsante di allocazione.")

