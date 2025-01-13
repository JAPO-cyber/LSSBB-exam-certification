import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM

# Funzione per caricare il modello leggero
@st.cache_resource
def load_light_model():
    tokenizer = AutoTokenizer.from_pretrained("distilgpt2")

    # Aggiungi un token di padding se non esiste
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': tokenizer.eos_token})

    model = AutoModelForCausalLM.from_pretrained("distilgpt2")
    model.resize_token_embeddings(len(tokenizer))  # Aggiorna la dimensione dell'embedding

    return tokenizer, model

# Inizializza l'app Streamlit
st.title("Streamlit App con Modello Leggero (Hugging Face)")
st.write("Inserisci un prompt e ottieni una risposta generata dal modello `distilgpt2`.")

# Carica modello e tokenizer
tokenizer, model = load_light_model()

# Input utente
user_input = st.text_area("Inserisci il tuo prompt:", placeholder="Scrivi qualcosa qui...")

# Generazione di testo
if st.button("Genera"):
    if user_input.strip():
        try:
            # Tokenizza il prompt
            inputs = tokenizer(user_input, return_tensors="pt", padding=True, truncation=True)

            # Genera la risposta
            outputs = model.generate(
                inputs["input_ids"],
                attention_mask=inputs.get("attention_mask"),  # Usa la maschera di attenzione se esiste
                pad_token_id=tokenizer.pad_token_id,  # Imposta esplicitamente il token di padding
                max_length=50,  # Limita la lunghezza massima della risposta
                num_return_sequences=1
            )

            # Decodifica e mostra il risultato
            if outputs:
                response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                st.subheader("Risultato Generato:")
                st.write(response)
            else:
                st.warning("Nessuna risposta generata. Prova a modificare il tuo prompt.")

        except Exception as e:
            st.error(f"Errore durante la generazione: {e}")
    else:
        st.warning("Per favore, inserisci un prompt valido prima di generare la risposta!")

