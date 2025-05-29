FROM python:3.11-slim

WORKDIR /streamlit

COPY requirements.txt ../streamlit
RUN pip install --no-cache-dir -r ../streamlit/requirements.txt

COPY . ../streamlit

EXPOSE 8080

CMD ["streamlit", "run", "connexion.py", "--browser.gatherUsageStats", "False", "--server.address", "0.0.0.0"]




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
