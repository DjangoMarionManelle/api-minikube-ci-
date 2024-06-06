# Utiliser une image de base Python officielle.
FROM python:3.8

# Définir le répertoire de travail dans le conteneur.
WORKDIR /app

# Copier les fichiers de dépendances.
COPY requirements.txt requirements.txt

# Installer les dépendances.
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers de l'application dans le conteneur.
COPY . .

# Informer Docker que l'application utilise le port 5000.
EXPOSE 5000

# Exécuter l'application.
CMD ["flask", "run", "--host=0.0.0.0"]


