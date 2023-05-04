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
list_deroulante_annees = list(liste_annees["startYear"])

# MACHINE LEARNING 
# Définir X
X = df_dummies_2.iloc[:,5:25000]
# On entraine notre modele uniquement sur les 4 voisin les plus proches sur l'ensemble des colonnes choisies
model_KNN_distance = NearestNeighbors(n_neighbors=4).fit(X)

# Choix du film 
films = st.selectbox("Films : ",list_film_deroulante_films)
st.write(films, ". Bon choix ;)")

# Subheader
st.subheader("Tu peux également choisir parmi les listes de choix suivantes")


# MULTI SELECT BOX : first argument takes the box title, second argument takes the options to show
                            
with st.form("form 3"):
        col1, col2, col3 = st.columns(3)
        with col1 :
            genres = st.multiselect(label = "Genres : ", options = list_film_deroulante_genres)
            st.write("Tu as choisis", len(genres), 'genre(s)')
        with col2 :
            acteurs = st.selectbox(label = "Acteurs : ", options = list_film_deroulante_acteurs)

        with col3 :
            start_year, end_year = st.select_slider(label = "Sélectionne une plage d'année",
                                    options=liste_annees["startYear"],
                                    value=(1913, 2023))
            st.write("Tu as choisis une plage d'année entre", start_year, 'et', end_year)
        submit = st.form_submit_button("Soumettre")

st.write("Vous avez choisi le film {}, les genres {}, ainsi que l'acteur/actrice {} entre les années {}".format(films, "/".join(genres), acteurs, str(start_year) +'-'+ str(end_year)))
st.write("je vous suggère fortement :")          

if submit : 
    # MACHINE LEARNING 
    #création d'une liste avec le film selectionné par l'utilisateur
            liste_du_film = [films]
        
    #obtenir tous les renseignements du film
            df_film_choisi = df_dummies_2[(df_dummies_2["primaryTitle"] == films) | (df_dummies_2["originalTitle"] == films)]
    
    # on ne selectionne que les colonnes contenant des booleens sur la ligne du film choisi
            film_choisi = df_film_choisi.iloc[:, 5:]
   
    #création de la matrice pour rechercher les 4 index des plus proches voisins (dont le film en question)
            distance, indice = model_KNN_distance.kneighbors(film_choisi)

    #création de la liste des suggestions à partir de la matrice
            suggestion = df_dummies_2.iloc[indice[0,1:]]['primaryTitle'].values
            st.write("On peut remplacer", films, "par :", suggestion)
  

# SOUS TITRE
st.subheader("Bon visionnage !")

