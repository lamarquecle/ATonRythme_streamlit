import streamlit as st
import os
#import subprocess
import requests
import json

st.set_page_config(
    page_title="Multipage App",
    page_icon="👋",
    layout="centered") # "wide : full page"

#####################################################################################################
#####################################################################################################
##################  DATABASE DU SERVEUR DE L ENTREPRISE  ############################################
#####################################################################################################
#####################################################################################################

@st.cache_data
def get_entreprise_server_datas():

    france_connaissances_non_connues = [
        "Probabilités",
        "Fonctions linéaires"]
    france_connaissances_connues = [[
        "Puissance d'un nombre",
        "Racine carrée",
        "Priorités opératoires",
        "Expressions littérales",
        "Equations du premier degré",
        "Catégories de triangles",
        "Construire un triangle",
        "Théorème de Pythagore",
        "Mesurer un segment"]][0]
    return france_connaissances_non_connues, france_connaissances_connues

france_connaissances_non_connues, france_connaissances_connues = get_entreprise_server_datas()
# Variables relatives au serveur de l'entreprise
    # connaissances_entree_connue -> connaissances_attendues_numerise_binar --APIprediction--> connaissances_attendues_denumerise
st.session_state.setdefault("france_connaissances_non_connues", france_connaissances_non_connues )
    # Permet d'avoir des pistes d'évolution de l'IA, cette variable doit être incrustée lorsque des
    # entrées de l'IA sont non reconues, une copie est aussi renvoyée pour chaque élèves en plus de la prédiction

st.session_state.setdefault("france_connaissances_connues", france_connaissances_connues)
    # ON ADMET DANS UN PREMIER TEMPS QUE L IA NE SE COMPOSE QUE D UN UNIQUE RESEAU DE NEURONES
    # = ["Pu", "RC", "Pr", "EL", "E", "CaT", "CoT", "TP", "MS"]


#####################################################################################################
#####################################################################################################
##################  DATABASE DE L ETABLISSEMENT SCOLAIRE  ###########################################
#####################################################################################################
#####################################################################################################
st.session_state.setdefault("etablissement_connaissances_non_connues", ["Probabilités"])

st.session_state.setdefault("etablissement_connaissances_connues", st.session_state["france_connaissances_connues"])
    # RQ : On admet que les compétences traitables par l'IA sont communiquées et connues par le serveur de l'établissement
    #st.session_state["etablissement_connaissances_connues"] = [
    #    i for i in france_connaissance_connue
    #        for france_connaissance_connue in st.session_state["france_connaissances_connues"]]

st.session_state.setdefault("volontes", ["Apprentissage", "Co-apprentissage", "Transmission", "Révisions"])


def have_etablissement_people():
    import random as rd
    import numpy as np
    import uuid
    def have_child(firstNames, lastNames):
        return {
            "firstName": firstNames,       "lastName": lastNames,
            "identifiant": "identifiant_x", "password": "password_x",
            "actual_role" : ["child"],
            "familly" : [],
            "uuid": str(uuid.uuid4()),
            "sexe": rd.choices(["M", "F"]), "class": {"5e4": 2005, "4e3": 2006},
            #"Knowledge":["Puissance d'un nombre","Priorités opératoires","Catégories de triangles","Probabilités"],
                # L'enseignant a une page pour remplir ces données et, les 2 autres compétences sont actualisées
            "knowledge_Model": np.random.randint( 0, 4, (1,9)).copy(),
            # RQ : ici structuré sous la forme connait ou non
            #      transformer futurement avec 0123 au format [0, 3, 2, 1, 0, 0, ...]
            #      avec "non acquis", "en cours d'acquisition", "acquis", "peut transmettre"
            #      dans notre modèle prédictif, on peut admettre que
            #           0 = ["non acquis", "en cours d'acquisition"]    1 = ["acquis", "peut transmettre"]
            "was_approached": np.random.randint( 1, 2, (1,9)).copy(),
            # Définit si l'élève s'est déjà penché sur le chapitre
            # NB : "(1, 2, (1, 9))" => on admet que tous les chapitres ont déjà été traité avec l'élève
            # NB : il peut-être concevable de fusionner "was_approached" et "knowledge_model" via M( : [0,1,2,3,4])
            "knowledge_NotModel" : {"Probabilités":2},
            "results" : [],
                # donne les résultats associés à chacuns des devoirs effectués pae l'élève
            "working_methods" : np.random.randint( 0, 2, (1,4)).copy(),
            # volontées de travail de l'élève
            "working_viabilities" : np.ones((1, 4)),
            # avis de l'enseignant sur la capacité de l'élève à faire parti d'une méthode de travail
            #"knowledge_viabilities" : np.ones( 0, 2, (1,9)).copy(),
            # chapitres devants être préfentiellement travaillés par l'élève selon l'enseignant (rq : variable peut-être associé à toute une classe)
            #"with_knowledge_viabilities" : True,
            # Envie de l'élève à mettre en avant les chapitres préconisés par l'enseignant
            "KOLB_results" : [],
            "DISC_results" : [],
            "comments": ""}

#########  VARIABLES RELATIVES A UNE SEANCE #########


##########  VARIABLES NIVEAU ETABLISSEMENT  #########


#####################
##    FRONT END    ##
#####################
with open('style.css') as file :
    st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)


import os

API_URL = os.getenv("API_URL")


#############################
##   CONNEXION FUNCTIONS   ##
#############################

CONSUMER_KEY    : str = ""
CONSUMER_SECRET : str = ""
SECURITY_TOKEN  : str = ""

def api_connect(API_URL  : str,
                username : str,
                password : str) -> str :

    username        : str = username
    password        : str = password
        # NB : les var "" sont actuellement non prises en compte par simplicité des premiers tests

    datas = {
        'grant_type'   : 'password',
        'client_id'    : CONSUMER_KEY,
        'client_secret': CONSUMER_SECRET,
        'username'     : username,
        'password'     : password + SECURITY_TOKEN}
    headers = {'Authorization': 'access_token token'}
    identification_encode = requests.post(
                                        API_URL + '/token',
                                        data    = datas,
                                        headers = headers)
        # RQ : la connection ne se fait actuellement que par "username" et "password"
        # pour une sécurité plus importante, d'autres champs peuvent être ajoutés
        # cf datas.client_id, security_token, ...

    if identification_encode .status_code != 200 :
        #assert identification_encode .status_code != 200, "Error into API access"
        return None
    else :
        identification = json.loads(identification_encode.content.decode())
        access_token   : str = str(identification["access_token"])
        return access_token
    # RQ : Si l'identification n'est pas bonne, une erreure ressort sur les prochains get
    #      car identification n'a pas "access_token" en clé

def get_user(API_URL      : str,
             access_token : str) -> dict :
    headers = {
            "accept"        : "application/json",
            "Authorization" : f'Bearer {access_token}'}
    user_encode = requests.get(API_URL  +'/users/me/items',
                               headers = headers)

    if user_encode.status_code != 200 :
        return None
    else :
        return json.loads(user_encode.content.decode())

def get_accessible_childs(API_URL      : str,
                          user_uuid    : str,
                          access_token : str) -> dict :
    headers = {
            "accept"        : "application/json",
            "Authorization" : f'Bearer {access_token}'}
    accessible_childs_encode = requests.get(API_URL + f'/user/{user_uuid}/childs',
                                            headers = headers)

    accessible_childs = accessible_childs_encode.json()
            # NB : childs = db_childs = {childs in the db}
            #      accessible_childs = {db_childs where a relation which user exist}   # <= etablissement_childs
            #      selected_childs = {accessible_childs selected by user's choice}     # <= seance_childs

    if accessible_childs_encode.status_code != 200 :
        return None
    else :
        return accessible_childs_encode.json()

def init_connexion( username : str,
                    password : str) -> tuple[str, str] :
    if password != "" : return username, password

    if username == "t":
        username = "username_0"
        password = "password_0"
    elif username == "p":
        username = "username_1"
        password = "password_1"
    elif username == "c":
        username = "username_5"
        password = "password_5"
    return username, password


##################################
##    FRONT END FOR CONNEXION   ##
##################################

username = st.text_input(label="Username",                )
password = st.text_input(label="Password", type="password")
        # NB : le paramètre key="password" n'est pas pris en compte en vue
        #      de l'utilisation de cette variable uniquement sur cette page
username, password = init_connexion( username, password)
        # RQ : Delete these lines more later (match-case invalid)

while True :
    if  len(username) > 50 or len(password) > 50 :
        st.warning("😕 For security, 'Username' and 'Password' must be under size 50")
        break
    if  not(username and password) :
        st.warning("😕 Please fill all the fields")
        break

    access_token = api_connect(API_URL, username , password)
    if  access_token is None :
        st.warning("😕 Error into API access")
        break
    st.session_state["access_token"]   = access_token

    user = get_user(API_URL, access_token)
    if  user is None :
        st.warning("😕 Error from API action")
        break
    st.session_state["identification"] = user


    user_uuid         = user["uuid"]
    accessible_childs = get_accessible_childs(API_URL, user_uuid, access_token)
    if  accessible_childs is None :
        st.warning("😕 Error to find your user's childs")
        break

    st.success('The assessment is created !', icon="✅")
    st.session_state["accessible_childs"] = accessible_childs.copy()
    st.session_state["selected_childs"  ] = accessible_childs.copy()
    break


#if __name__ == "__main__":
#    subprocess.run(["streamlit", "run", "connexion.py", "--browser.gatherUsageStats", "False", "--server.address", "0.0.0.0"])

0*"""
import numpy as np
from tensorflow import keras
from keras.models import load_model
model_file = "models/can_learn_model.h5"
model = load_model(model_file)

st.write(model.layers[1].get_config())
st.write(model.layers[1].input_shape)
st.write(model.layers[1].output_shape)
a,b = model.layers[1].get_weights()
st.write(np.around(a,2))
st.write(np.around(b,2))
st.write(model.layers[1].trainable)
st.write(model)

a,b = model.layers[0].get_weights()
st.write(np.around(a,2))
st.write(np.around(b,2))
"""
