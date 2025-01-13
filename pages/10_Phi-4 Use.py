import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM

# Funzione per caricare il modello e il tokenizer
@st.cache_resource
def load_phi4_model():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-4", trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained("microsoft/phi-4", trust_remote_code=True)
    return tokenizer, model

# Inizializza Streamlit
st.title("Streamlit App with Microsoft Phi-4")
st.write("Inserisci un prompt e ottieni una risposta generata dal modello Phi-4.")

# Carica modello e tokenizer
tokenizer, model = load_phi4_model()

# Input utente
user_input = st.text_area("Inserisci il tuo prompt qui:", placeholder="Scrivi qualcosa...")

# Generazione del testo
if st.button("Genera"):
    if user_input.strip():
        # Tokenizza l'input
        inputs = tokenizer(user_input, return_tensors="pt")
        
        # Genera la risposta
        outputs = model.generate(inputs["input_ids"], max_length=100, num_return_sequences=1)
        
        # Decodifica la risposta
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Mostra la risposta
        st.subheader("Risposta generata:")
        st.write(response)
    else:
        st.warning("Per favore, inserisci un prompt prima di generare la risposta!")
