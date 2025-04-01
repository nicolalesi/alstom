# Usa una base image di Python
FROM python:3.10

# Installa le dipendenze necessarie
RUN pip install pandas openpyxl ollama

# Imposta la directory di lavoro nel container
WORKDIR /app

# Copia il tuo codice e gli altri file necessari nella cartella /app
COPY . /app

# Comando predefinito per eseguire il tuo script Python
CMD ["python"]
