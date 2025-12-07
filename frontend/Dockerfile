# 1. Wir starten mit einem Linux, auf dem Node.js (Version 20) drauf ist
FROM node:20-alpine

# 2. Arbeitsordner im Container
WORKDIR /app

# 3. Zuerst die Paket-Dateien kopieren
COPY package.json package-lock.json ./

# 4. Pakete installieren (wie 'npm install')
RUN npm install

# 5. Den Rest des Codes kopieren
COPY . .

# 6. Den Server starten
# host 0.0.0.0 ist hier auch extrem wichtig!
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]