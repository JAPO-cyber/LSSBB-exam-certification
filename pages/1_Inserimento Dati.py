with tabs[1]:
    st.title("Modifica Dati")

    df = load_data()
    if df.empty:
        st.warning("Non ci sono dati disponibili per la modifica.")
    else:
        st.write("Dati attualmente salvati:")
        st.dataframe(df)

        # Selezione della riga da modificare
        row_index = st.number_input("Seleziona la riga da modificare (0 per la prima)", min_value=0, max_value=len(df)-1, step=1)
        st.write("Riga selezionata:")
        st.write(df.iloc[row_index])

        with st.form("edit_form"):
            # Campi per la modifica
            nome = st.text_input("Nome", df.iloc[row_index]["Nome"])
            età = st.number_input("Età", min_value=0, step=1, value=int(df.iloc[row_index]["Età"]))
            altezza = st.number_input("Altezza (in cm)", min_value=0.0, step=0.1, value=float(df.iloc[row_index]["Altezza (cm)"]))
            descrizione = st.text_area("Descrizione", df.iloc[row_index]["Descrizione"])
            genere = st.selectbox("Genere", ["Maschio", "Femmina", "Altro"], index=["Maschio", "Femmina", "Altro"].index(df.iloc[row_index]["Genere"]))
            hobby = st.text_area("Hobby (separati da --)", value=df.iloc[row_index]["Hobby"])
            fermi = df.iloc[row_index].get("Fermi", "")
            if pd.isna(fermi):
                fermi = ""
            fermi = st.text_area("Fermi (separati da --)", value=fermi)

            giorno = st.date_input(
                "Giorno", 
                value=pd.to_datetime(df.iloc[row_index]["Giorno"], errors="coerce").date() if "Giorno" in df.columns and pd.notna(df.iloc[row_index]["Giorno"]) else datetime.today().date()
            )
            durata = st.number_input(
                "Durata (minuti)", 
                min_value=0, 
                step=1, 
                value=int(df.iloc[row_index]["Durata"]) if "Durata" in df.columns and pd.notna(df.iloc[row_index]["Durata"]) else 0
            )

            # Campo "Ora Orologio" con HTML personalizzato
            st.subheader("Ora Orologio")
            ora_corrente = df.iloc[row_index].get("Ora Orologio", "12:00")
            ora_corrente = ora_corrente if pd.notna(ora_corrente) else "12:00"
            ora_orologio_html = f"""
            <label for="timeInput" style="font-size: 16px; color: white;">Ora Orologio:</label>
            <input type="time" id="timeInput" value="{ora_corrente}" style="font-size: 18px; padding: 5px; background-color: black; color: white; border: 1px solid white; border-radius: 4px;">
            """
            st.components.v1.html(ora_orologio_html, height=70)

            # Pulsante per salvare le modifiche
            save_button = st.form_submit_button("Salva Modifiche")

        if save_button:
            # Salvataggio dei dati aggiornati
            df.at[row_index, "Nome"] = nome
            df.at[row_index, "Età"] = età
            df.at[row_index, "Altezza (cm)"] = altezza
            df.at[row_index, "Descrizione"] = descrizione
            df.at[row_index, "Genere"] = genere
            df.at[row_index, "Hobby"] = hobby
            df.at[row_index, "Fermi"] = fermi
            df.at[row_index, "Giorno"] = giorno
            df.at[row_index, "Durata"] = durata
            df.at[row_index, "Ora Orologio"] = ora_corrente  # Puoi gestire il recupero del valore selezionato dall'HTML

            save_data(df)
            st.success("Modifiche salvate con successo!")
            st.dataframe(df)


