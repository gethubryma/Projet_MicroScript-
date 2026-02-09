# --- ÉTAPE 1: La phase de "Build" ---
# On utilise une image Node.js légère pour construire le projet
FROM node:20-alpine AS builder

# On définit le répertoire de travail dans le conteneur
WORKDIR /app

# On copie les fichiers de dépendances pour profiter du cache de Docker
COPY package*.json ./

# On installe les dépendances du projet
RUN npm install

# On copie tout le reste du code source
COPY . .

# On lance la commande de build pour générer les fichiers statiques
RUN npm run build

# --- ÉTAPE 2: La phase de "Production" ---
# On part d'une image Nginx très légère pour servir nos fichiers
FROM nginx:stable-alpine

# On copie uniquement les fichiers construits de l'étape précédente
# dans le dossier par défaut de Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# On expose le port 80, sur lequel Nginx écoute
EXPOSE 80

# La commande pour démarrer Nginx quand le conteneur se lance
CMD ["nginx", "-g", "daemon off;"]