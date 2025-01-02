import streamlit as st

# Stato del login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login
if not st.session_state.logged_in:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.success("Accesso effettuato con successo!")
        else:
            st.error("Credenziali errate. Riprova.")
else:
    # Mostra contenuto post-login
    st.title("Benvenuto!")
    st.write("Hai effettuato l'accesso con successo.")
    
    # Pulsante di logout
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.clear()

