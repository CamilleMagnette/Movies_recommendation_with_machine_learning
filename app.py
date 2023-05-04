# A METTRE DANS JUPITER 
# Commande qui permet d'écrire dans le fichier app.py
# %%writefile app.py

# IMPORTER LES LIBRAIRIES
import streamlit as st
import pandas as pd 
from sklearn.neighbors import NearestNeighbors
from sklearn import datasets

# IMPORTER LES DATAFRAMES UTILISES
liste_films = pd.read_pickle("liste_films.pkl.gz")
liste_genres = pd.read_pickle("liste_genres.pkl.gz")
liste_acteurs = pd.read_pickle("liste_acteurs.pkl.gz")
liste_annees = pd.read_pickle("liste_annees.pkl.gz")
df_dummies_2 = pd.read_pickle("df_dummies_2.pkl.gz")

# CONFIGURER LA PAGE
st.set_page_config(
    page_title="Recommandation de Film App",
    layout="wide",
    page_icon=":🎞️:")

# TITRE
st.title("Application de recommandation de films")

# SOUS TITRE
st.header("Dis moi quel film tu aimes et je t'en ferai aimer d'autres")

# Subheader
st.subheader("Choisi obligatoirement ton film préféré")

# LISTES 
list_film_deroulante_films = ["Tape le film que tu aimes"] + list(liste_films["primaryTitle"])
list_film_deroulante_acteurs = ["Choisis un acteur que tu aimes"] + list(liste_acteurs["primaryName"])
list_film_deroulante_genres = list(liste_genres["genres"])
list_deroulante_anneeS = list(liste_annees["startYear"])

# MULTI SELECT BOX : first argument takes the box title, second argument takes the options to show
                            
with st.form("form 4"):
        col1, col2, col3, col4 = st.columns(4)
        with col1 :
            films = st.selectbox("Films : ", list_film_deroulante_films)
        with col2 :
            genres = st.multiselect("Genres : ", liste_genres)
        with col3 :
            acteurs = st.selectbox("Acteurs : ", list_film_deroulante_acteurs)
        with col4 :
            start_year, end_year = st.select_slider('Années',
                                    options=liste_annees["startYear"],
                                    value=(1913, 2023))
        submit = st.form_submit_button("Soumettre")
 
if submit : 
    st.write("Vous avez choisi le film {}, les genres {}, ainsi que l'acteur/actrice {} entre les années {}".format(films, "/".join(genres), acteurs, str(start_year) +'-'+ str(end_year)))
    st.write("je vous suggère fortement :")

    # SOUS TITRE
st.subheader("Bon visionnage !")
