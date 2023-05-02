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
liste_annees = pd.read_pickle("liste_annees.pkl.gz")

# CONFIGURER LA PAGE
st.set_page_config(
    page_title="Recommandation de Film App",
    layout="wide",
    page_icon=":🎞️:")

# TITRE
st.title("Application de remmandation de films")

# SOUS TITRE
st.header("Dis moi quel film tu aimes et je t'en ferai aimer d'autres")

# MULTI SELECT BOX : first argument takes the box title, second argument takes the options to show

list_film_deroulante_films = ["Tape le film que tu aimes"] + list(liste_films["primaryTitle"])
list_film_deroulante_genres = ["Choisis les genres que tu aimes"] + list(liste_genres["genres"])
list_film_deroulante_acteurs = ["Choisis un acteur que tu aimes"] + list(liste_acteurs["primaryName"])

                                      
with st.form("form 4"):
        col1, col2, col3, col4 = st.columns(4)
        with col1 :
            films = st.selectbox("Films : ", list_film_deroulante_films)
            st.write("Tu as choisis : ", films, ". Bon choix ;)")
        with col2 :
            genres = st.multiselect("Genres : ", list_film_deroulante_genres)
        with col3 :
            acteurs = st.selectbox("Acteurs : ", list_film_deroulante_acteurs)
        with col4 :
            start_year, end_year = st.select_slider('Années',
                                    options=liste_annees["startYear"],
                                    value=(1913, 2023))
            st.write('Vous avez choisi les années entre', start_year, 'et', end_year)
        submit : st.form_submit_button("Soumettre")
 
#if submit : 
#    st.write("Tu as choisi le film : ", films, " , le genre : ", genres ,"entre les années", start_year ,"et", end_year) 

# SOUS TITRE
st.subheader("Bon visionnage !")
