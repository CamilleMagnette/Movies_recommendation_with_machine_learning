# A METTRE DANS JUPITER 
# Commande qui permet d'écrire dans le fichier app.py
# %%writefile app.py

# IMPORTER LES LIBRAIRIES
import streamlit as st
import pandas as pd 

# IMPORTER LES DATAFRAMES UTILISES
liste_films = pd.read_pickle("liste_films.pkl.gz")
liste_genres = pd.read_pickle("liste_genres.pkl.gz")
liste_acteurs = pd.read_pickle("liste_acteurs.pkl.gz")


# CONFIGURER LA PAGE
st.set_page_config(
    page_title="Recommandation de Film App",
    layout="wide",
    page_icon=":🎞️:")

# TITRE
st.title("Bienvenue dans notre humble application de remmandation de film")

# SOUS TITRE
st.header("Dis moi quel film tu aimes et je t'en ferai aimer d'autres")

# MULTI SELECT BOX : first argument takes the box title, second argument takes the options to show

list_film_deroulante = ["Tape le film que tu aimes"] + list(liste_films["primaryTitle"])

with st.form("form 4"):
        col1, col2, col3, col4 = st.columns(4)
        with col1 :
            films = st.selectbox("Films : ", list_film_deroulante)
            st.write("Tu as choisis : ", films, ". Bon choix ;)")
        with col2 :
            genres = st.multiselect("Genres : ", liste_genres)
            st.write("Tu as choisis", len(genres), 'genre(s)')
        with col3 :
            acteurs = st.multiselect("Acteurs : ", liste_acteurs)
            st.write("Tu as choisis", len(acteurs), 'acteur(trice)')
        with col4 :
            année = st.slider("Année", 1913, 2023)
            st.text('Choisie : {}'.format(année))
        submit : st.form_submit_button("Soumettre")
        
# SOUS TITRE
st.subheader("Bon visionnage !")
