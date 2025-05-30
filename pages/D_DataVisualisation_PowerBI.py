import streamlit as st
import os

DASHBOARD_URL = os.getenv("DASHBOARD_URL")
SIZE_WINDOW   = {"width" :"960px",
                 "height":"776px"}
                 #

html_string = f'''<iframe title="DataVisualisation" width="{SIZE_WINDOW['width']}" height="{SIZE_WINDOW['width']}" src="{DASHBOARD_URL}" frameborder="0" allowFullScreen="true"></iframe>'''
st.markdown(html_string, unsafe_allow_html=True)
0*'''
    a. Créer un compte powerBI avec un courriel professionnel


    1. Crééer un 'report' sur powerBI desktop
    1' Aller dans 'view' -> 'fit to width' afin de planifier la taille d'affichage du 'report' sur le site avant la publication
    2. Utiliser l'onglet 'publier' de PowerBI desktop pour transferer le 'report' sur powerBI Service
    3. Sur PowerBI Service, entrer dans le Dashboard importé puis utiliser 'File' -> 'Embed report' -> 'website or portal'
       pour obtenir le code html permettant d'importer le Dashboard sur un site internet'''

