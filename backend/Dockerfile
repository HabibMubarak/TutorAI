# 1. Wir starten mit einem leichten Linux, auf dem Python 3.10 schon drauf ist
FROM python:3.10-slim

# 2. Das ist unser Arbeitsordner im Container
WORKDIR /app

# 3. Zuerst kopieren wir NUR die Einkaufsliste (Caching-Trick!)
COPY requirements.txt .

# 4. Jetzt installieren wir die Python-Pakete
# --no-cache-dir hält das Image klein
RUN pip install --no-cache-dir -r requirements.txt

# 5. Jetzt kopieren wir den Rest des Codes
COPY . .

# 6. Dieser Befehl startet den Server
# host 0.0.0.0 ist wichtig, damit Docker von außen drauf zugreifen darf
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]