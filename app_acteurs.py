# IMPORTS

# IMPORTER LES LIBRAIRIES
import streamlit as st
import pandas as pd 
from sklearn.neighbors import NearestNeighbors
#from sklearn import datasets
#from sklearn.preprocessing import StandardScaler
import requests
from sklearn.preprocessing import MinMaxScaler


# IMPORTER LES DATAFRAMES UTILISES QUAND ON EST SUR GIT HUB
liste_films = pd.read_pickle("./Databases/liste_films.pkl.gz")
liste_genres = pd.read_pickle("./Databases/liste_genres.pkl.gz")
liste_acteurs = pd.read_pickle("./Databases/liste_acteurs.pkl.gz")
liste_annees = pd.read_pickle("./Databases/liste_annees.pkl.gz")
df_machine_learning_clean = pd.read_pickle("./Databases/df_machine_learning_clean.pkl.gz")

# IMPORTER LES DATAFRAMES UTILISES QUAND ON EST EN LOCAL 
#liste_films = pd.read_pickle("./FICHIERS POUR MACHINE LEARNING/liste_films.pkl.gz")
#liste_genres = pd.read_pickle("./FICHIERS POUR MACHINE LEARNING/liste_genres.pkl.gz")
#liste_acteurs = pd.read_pickle("./FICHIERS POUR MACHINE LEARNING/liste_acteurs.pkl.gz")
#liste_annees = pd.read_pickle("./FICHIERS POUR MACHINE LEARNING/liste_annees.pkl.gz")
#df_machine_learning_clean = pd.read_pickle("./df_machine_learning_clean.pkl.gz")

# SUPPRIMER LES DOUBLONS
df_machine_learning_clean = df_machine_learning_clean.drop_duplicates(subset = "tconst")



# CONFIGURER LA PAGE

st.set_page_config(
    page_title="Recommandation de Film App",
    layout="wide",
    page_icon=":🎞️:")

# TITRE
st.title("🎥 Recommandation de films")

# SOUS TITRE
st.header("Dis moi quels sont tes goûts et je te ferai découvrir de nouveaux films 💡🎬")

# MISE EN FORME FOND DE PAGE 
page_bg_img = """
<style>
[data-testid = "stAppViewContainer"] {
background-color: #e5e5f7;
opacity: 0.8;
background-image: radial-gradient(#444cf7 0.5px, #e5e5f7 0.5px);
background-size: 10px 10px; }
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html = True)



# LISTES 

list_film_deroulante_films = ["Tape le film que tu aimes"] + list(liste_films["primaryTitle"])
list_film_deroulante_acteurs = ["Choisis un acteur que tu aimes"] + list(liste_acteurs["primaryName"])
list_film_deroulante_genres = list(liste_genres["genres"])



# REQUETE API 

# site : https://www.omdbapi.com/
# demande de key API : key = aa10e4e0
url_api = "http://www.omdbapi.com/?i="
key_api = "&apikey=aa10e4e0"
url_imdb = 'https://www.imdb.com/title/' # pour afficher le lien sur le site


# MACHINE LEARNING : 
# Recommandation sur la base du nom d'un film (tconst) en se basant sur les paramètres numériques suivants : startYear, runtimeMinutes, averageRating, numVotes, genres et acteurs

# Standardisation : on harmonise l'échelle des abscisses et des ordonnées =>  On réindice l'ensemble des valeurs pour rentrer dans le même cadre d'analyse et réaliser des classifications. 
scaling = MinMaxScaler()
df_machine_learning_clean[["averageRating", "numVotes", "runtimeMinutes", "startYear"]] = scaling.fit_transform(df_machine_learning_clean[["averageRating", "numVotes", "runtimeMinutes", "startYear"]])

# Récupération des noms des colonnes sans prendre tconst + primaryTitle + originalTitle + French_Title 
colonnes_ml = df_machine_learning_clean.columns[4:]

# Création de la variable X qui prends en variables explicatives toutes les colonnes avec des valeurs boléennes - PAS BESOIN DE SCALER => toutes les lignes et toutes les colonnes à partir d'index 8 
# X = df_machine_learning_clean.iloc[:,8:] 

# Création de la variable X qui prends en variables explicatives toutes les colonnes numériques et boléennes sauf (voir celles ci-dessus)
X = df_machine_learning_clean.loc[:, colonnes_ml]

# On entraine notre modele uniquement sur les 4 voisin les plus proches sur l'ensemble des colonnes choisies (metric = calcul de la distance avec le calcul cosinus)
model_KNN_distance = NearestNeighbors(n_neighbors = 4, metric = "cosine", algorithm = "brute").fit(X)



# CHOIX DU FILM PAR L'UTILISATEUR

with st.form("form 1"):
    
    # Indication utilisateur
    st.subheader("OPTION 1 : Choisi ton film préféré ♥️ et selectionne 'Soumettre'")
        
    # Mise en place du choix utilisateurs
    films = st.selectbox("Films : ",list_film_deroulante_films)

    # Bouton submit
    submit_1 = st.form_submit_button("Soumettre")

        
    # PROPOSITION DE L'ALGORITHME

    if submit_1 : 

        # Obtenir tous les renseignements du film
        df_film_choisi = df_machine_learning_clean[(df_machine_learning_clean["primaryTitle"] == films) | (df_machine_learning_clean["originalTitle"] == films) | (df_machine_learning_clean["French_Title"] == films)]

        # On ne selectionne que les colonnes contenant des booleens sur la ligne du film choisi
        film_choisi = df_film_choisi.iloc[:, 4:]

        #création de la matrice pour rechercher les 4 index des plus proches voisins (dont le film en question)
        distance, indice = model_KNN_distance.kneighbors(film_choisi)

        # Création d'une variable tconst pour récupérer le numéro tconst du film
        tconst = df_machine_learning_clean.iloc[indice[0,1:]]['tconst'].values
        #st.write("On peut remplacer", films, "par :", tconst)

        # Création de la liste des suggestions à partir de la matrice
        suggestion = df_machine_learning_clean.iloc[indice[0,1:]]['primaryTitle'].values
        #st.write("On peut remplacer", films, "par :", suggestion)

        # Création de colonnes
        col1 = st.columns(3)

        # Boucle simultanée sur les deux paramètres : suggestion et tconst 
        for films, code_film, colonnes in zip(suggestion,tconst, col1):

            with colonnes:

                url = url_api + str(code_film) + key_api  
                url_imdb2 = url_imdb + str(code_film)
                try:
                    response = requests.get(url)
                    #st.write(str(url))       
                    response.raise_for_status()
                    data = response.json()
                    url_image = data['Poster']
                    st.image(url_image, width=200)

                except requests.exceptions.RequestException as e:
                    print('Une erreur est survenue lors de l\'appel à l\'API :', e)
 
                # Pour ajouter le lien du site imdb
                if type(films) == str:
                    st.write(f" - [{films}]({url_imdb2})")
                else:
                    st.write(f" - [{films}]({url_imdb2})")

# Résultat de la requete avec le tconst choisi = fichier jason = DATA 
#{"Title":"Intolerance","Year":"1916","Rated":"Passed","Released":"15 Jun 1917","Runtime":"163 min","Genre":"Drama, History","Director":"D.W. Griffith","Writer":"Hettie Grey Baker, Tod Browning, D.W. Griffith","Actors":"Lillian Gish, Robert Harron, Mae Marsh","Plot":"The story of a poor young woman separated by prejudice from her husband and baby is interwoven with tales of intolerance from throughout history.","Language":"English","Country":"United States","Awards":"2 wins","Poster":"https://m.media-amazon.com/images/M/MV5BZTc0YjA1ZjctOTFlZi00NWRiLWE2MTAtZDE1MWY1YTgzOTJjXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.7/10"},{"Source":"Rotten Tomatoes","Value":"97%"},{"Source":"Metacritic","Value":"99/100"}],"Metascore":"99","imdbRating":"7.7","imdbVotes":"16,027","imdbID":"tt0006864","Type":"movie","DVD":"07 Dec 1999","BoxOffice":"N/A","Production":"N/A","Website":"N/A","Response":"True"}



# CHOIX DU GENRE, DE L'ACTEUR ET DE LA PERIODE SOUHAITEE PAR L'UTILISATEUR
                            
with st.form("form 2"):
    
    # Indication utilisateur
    st.subheader("OPTION 2 : Tu peux également choisir tes genres et ton acteur préférés sur une période souhaitée 🕺⭐")
    
    # Mise en place des choix utilisateurs
    col1, col2, col3 = st.columns(3)
    with col1 :
        start_year, end_year = st.select_slider(label = "Période",
                                    options=liste_annees["startYear"],
                                    value=(1913, 2023))
        st.write("Tu as choisis la période de ", start_year, 'à', end_year)

    with col2 :
        acteurs = st.selectbox(label = "Acteurs : ", options = list_film_deroulante_acteurs)

    with col3 :
        genres = st.multiselect(label = "Genres : ", options = list_film_deroulante_genres)
        st.write("Tu as choisis", len(genres), 'genre(s)')
    
    # bouton submit
    submit_2 = st.form_submit_button("Soumettre")

    
    if submit_2 : 

        df_machine_learning_clean_year = pd.merge(liste_annees[liste_annees['startYear'].between(start_year, end_year)], df_machine_learning_clean, how = 'left', left_on = 'tconst', right_on = 'tconst')  

        
        #Créer un DF filtré SUR L'ACTEUR renseigné par l'utilisateur
        #df_year_actor_choisi = df_machine_learning_clean_year[ (df_machine_learning_clean_year[acteurs] == True) & (df_machine_learning_clean_year["startYear"] >= start_year) & (df_machine_learning_clean_year["startYear"] <= end_year) ]
        df_year_actor_choisi = df_machine_learning_clean_year[(df_machine_learning_clean_year[acteurs] == True)]
        
        #Créer un DF filtré SUR LA PERIODE ET LE GENRE renseignés par l'utilisateur
        df_year_genre_choisi = pd.DataFrame()
        for genre in genres : 
            #df_genre= df_machine_learning_clean_year[ (df_machine_learning_clean_year[genre] == True) & (df_machine_learning_clean_year["startYear"] >= start_year) & (df_machine_learning_clean_year["startYear"] <= end_year) ]
            df_genre= df_machine_learning_clean_year[ (df_machine_learning_clean_year[genre] == True) ]
            
            df_year_genre_choisi = pd.concat([df_year_genre_choisi , df_genre])


            
        # Classer dans l'ordre decroissant la colonne averageRating
        df_year_actor_choisi = df_year_actor_choisi.sort_values(by ='averageRating' , ascending = False)
        df_year_genre_choisi = df_year_genre_choisi.sort_values(by ='averageRating' , ascending = False)

        # TOP 3 des films acteurs classés par note
        df_top3_acteur_choisi = df_year_actor_choisi.head(3)
        df_top3_genre_choisi = df_year_genre_choisi.head(3)

        # On récupère uniquement les codes films tconst 
        tconst_acteur = df_top3_acteur_choisi.iloc[:,:]['tconst'].values
        tconst_genre = df_top3_genre_choisi.iloc[:,:]['tconst'].values

        # On récupère uniquement les nom des films  
        suggestion_acteur = df_top3_acteur_choisi.iloc[:,:]['primaryTitle'].values
        suggestion_genre = df_top3_genre_choisi.iloc[:,:]['primaryTitle'].values

        # Prendre en compte l'absence d'acteur renseigné par l'utilisateur 
        if acteurs != "Choisis un acteur que tu aimes":

            # Indication utilisateur
            st.subheader("Si vous aimez {} je vous suggère fortement les 3 films suivants :".format(acteurs)  ) 

            # Création de colonnes
            col1 = st.columns(3)

            # PROPOSITION ACTEUR => Boucle simultanée sur les deux paramètres : suggestion et tconst 
            for films_acteur, code_film_acteur, colonnes_acteur in zip(suggestion_acteur,tconst_acteur, col1):

                with colonnes_acteur:

                    url1 = url_api + str(code_film_acteur) + key_api   # on remplace tconst par code_film
                    url1_imdb2 = url_imdb + str(code_film_acteur)

                    try:
                        response = requests.get(url1)
                        #st.write(str(url))       
                        response.raise_for_status()
                        data = response.json()
                        url_image = data['Poster']
                        st.image(url_image, width=200)

                    except requests.exceptions.RequestException as e:
                        print('Une erreur est survenue lors de l\'appel à l\'API :', e)

                    # Pour ajouter le lien du site imdb
                    if type(films_acteur) == str:
                        st.write(f" - [{films_acteur}]({url1_imdb2})")
                    else:
                        st.write(f" - [{films_acteur}]({url1_imdb2})")
                        
                        
        # Prendre en compte l'absence de genres renseignés par l'utilisateur 
        if genres != []:

            # Indication utilisateur
            st.subheader("Compte tenu des genres que vous appréciez, je vous suggère également les 3 films suivants :" ) 

            # Création de colonnes
            col2 = st.columns(3) 

            # PROPOSITION GENRE ET ANNEES => Boucle simultanée sur les deux paramètres : suggestion et tconst 
            for films_genre, code_film_genre, colonnes_genre in zip(suggestion_genre,tconst_genre, col2):

                with colonnes_genre:

                    url2 = url_api + str(code_film_genre) + key_api   # on remplace tconst par code_film
                    url2_imdb2 = url_imdb + str(code_film_genre)

                    try:
                        response = requests.get(url2)
                        #st.write(str(url))       
                        response.raise_for_status()
                        data = response.json()
                        url_image = data['Poster']
                        st.image(url_image, width=200)

                    except requests.exceptions.RequestException as e:
                        print('Une erreur est survenue lors de l\'appel à l\'API :', e)

                    # Pour ajouter le lien du site imdb
                    if type(films_genre) == str:
                        st.write(f" - [{films_genre}]({url2_imdb2})")
                    else:
                        st.write(f" - [{films_genre}]({url2_imdb2})")
    
    
    

# SOUS-TITRE
st.subheader("Bon visionnage ! 🍿🍿🍿 ")
