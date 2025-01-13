import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM

# Funzione per caricare il modello leggero
@st.cache_resource
def load_light_model():
    tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
    model = AutoModelForCausalLM.from_pretrained("distilgpt2")
    return tokenizer, model

# Inizializza l'app Streamlit
st.title("Streamlit App con Modello Leggero (Hugging Face)")
st.write("Inserisci un prompt e ottieni una risposta generata da `distilgpt2`.")

# Carica modello e tokenizer
tokenizer, model = load_light_model()

# Input utente
user_input = st.text_area("Inserisci il tuo prompt:", placeholder="Scrivi qualcosa qui...")

# Generazione di testo
if st.button("Genera"):
    if user_input.strip():
        # Tokenizza il prompt
        inputs = tokenizer(user_input, return_tensors="pt")
        
        # Genera la risposta
        outputs = model.generate(inputs["input_ids"], max_length=50, num_return_sequences=1)
        
        # Decodifica e mostra il risultato
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        st.subheader("Risultato Generato:")
        st.write(response)
    else:
        st.warning("Per favore, inserisci un prompt prima di generare la risposta!")
