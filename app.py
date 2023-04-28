# A METTRE DANS JUPITER 
# Commande qui permet d'écrire dans le fichier app.py
# %%writefile app.py

# IMPORTER LA LIVRAIRIE
import streamlit as st

# CONFIGURER LA PAGE
st.set_page_config(
    page_title="Recommandation de Film App",
    layout="wide",
    page_icon=":🎞️:")

#title
st.title("Bienvenue dans notre humble application de remmandation de film")

# Header
st.header("Dis moi quel film tu aimes et je t'en ferai aimer d'autres")

# multi select box
# first argument takes the box title
# second argument takes the options to show
with st.form("form 4"):
        col1, col2, col3, col4 = st.columns(4)
        with col1 :
            films = st.selectbox("Films : ", ['Dis moi quel film tu aimes', 'Film1', 'film2', 'film3'])
            st.write("Tu as choisis : ", films, ". Bon choix ;)")
        with col2 :
            genres = st.multiselect("Genres : ", ["Drama", "Comedy,Drama", "Drama,Romance", "Documentary", "Comedy"])
            st.write("Tu as choisis", len(genres), 'genre(s)')
        with col3 :
            acteurs = st.multiselect("Acteurs : ", ["Leo", "Alain", "Clint", "Marylin"])
            st.write("Tu as choisis", len(acteurs), 'acteur(trice)')
        with col4 :
            année = st.slider("Année", 1913, 2023)
            st.text('Choisie : {}'.format(année))
        submit : st.form_submit_button("Soumettre")
        
# Subheader
st.subheader("Bon visionnage !")
