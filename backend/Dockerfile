# Dockerfile pour le langage de programmation français
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Mettre à jour pip
RUN pip install --upgrade pip

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Exposer le port 5000
EXPOSE 5000

# Variables d'environnement
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=5000

# Commande pour démarrer l'application
CMD ["python", "app.py"]
