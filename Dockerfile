# Usa un'immagine base di Python
FROM python:3.9-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file di dipendenza
COPY app/requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'applicazione
COPY app/ .

# Esponi la porta 5000
EXPOSE 5000

# Comando per avviare l'applicazione
CMD ["python", "app.py"]