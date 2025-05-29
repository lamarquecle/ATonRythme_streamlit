FROM python:3.11

EXPOSE 8080
WORKDIR /streamlit

COPY . ./
ENV API_URL="https://atonrythme-fastapi-800884171084.europe-west1.run.app"

RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "connexion.py", "--server.port=8080", "--server.address=0.0.0.0"]




# Utiliser une image de base Python officielle
#FROM python:3.9.4-slim

# création du fichier streamlit
#RUN mkdir /streamlit

# Copier le fichier requirements.txt dans le fichier /streamlit conteneur
#COPY requirements.txt /streamlit

# Définir le répertoire de travail dans le conteneur
#WORKDIR /streamlit

# Installer les dépendances
#RUN pip install -r requirements.txt

# Install make for Makefile
#RUN set -xe \
#    && apk add --no-cache --virtual \
#    make

# Copier le fichier dans le fichier streamlit du conteneur
#COPY . /streamlit

#EXPOSE 8501

#CMD ["streamlit", "run", "connexion.py", "--browser.gatherUsageStats", "False", "--server.address", "0.0.0.0"]
