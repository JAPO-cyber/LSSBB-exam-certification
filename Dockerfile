# Usa un'immagine base di Python leggera
FROM python:3.9-slim

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia tutti i file e le cartelle nella directory del container
COPY . /app

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Espone la porta usata da Streamlit
EXPOSE 8501

# Comando di avvio per l'app Streamlit
CMD ["streamlit", "run", "LSSBB_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
