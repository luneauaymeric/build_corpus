import streamlit as st
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import grouping_post as gp
import visualisation
import convert
#import streamlit as st
#from tkinter import filedialog
#import glob

# Script inspired from https://github.com/emilienschultz/dstool

# Fonction pour afficher les "topics disponibles"
def topics(data,topic_column):
    d_topic = data.groupby([topic_column]).agg(nb = ("id", "size")).sort_values("nb", ascending=False).reset_index()
    list_topics = [x for x in d_topic[topic_column].unique()]
    return list_topics




@st.cache_data # évite que cette fonction soit exécutée à chaque fois
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')



#  Chargement du CSV contenant les tweets (un seul fichier à la fois)
st.sidebar.title("Chargement d'un fichier CSV")
uploaded_files = st.sidebar.file_uploader("Téléverser le fichier csv", accept_multiple_files=False)


if uploaded_files is not None:
    path_in = uploaded_files.name
    print(path_in)
else:
    path_in = None

st.sidebar.divider()
if uploaded_files is not None:
    df = gp.df_processor(uploaded_files)

    st.sidebar.write("Nombre de textes: ", len(df))

    #buildcorpus = st.sidebar.write("Opérer un regroupement")
    st.sidebar.write("Opérer un regroupement")
    number = st.sidebar.number_input('Nombre minimum de mot')
    minute_interval = st.sidebar.number_input("Définir l'intervale de temps (en minute)",value=30) #on concatène tous les textes publiés dans cet intervale
    submit = st.sidebar.button(f'Regrouper')


    fig = visualisation.tracer_graphique(data = df, d = "Jour")
    tab1, tab2 = st.tabs(["Texte", "Tableau"])
    with tab1 :
        timeserie = st.pyplot(fig)
        st.divider()
        placeholder = st.empty()
        container = st.container()
        with placeholder.container():
            show_text = visualisation.display_text(data=df)
    with tab2:
        placeholder2 = st.empty()
        container2 = st.container()
        with placeholder2.container():
            st.dataframe(data=df)

    if submit :
        new_df = gp.group_by_user_by_minute(df, number, minute_interval)
        with placeholder2.container():
            st.dataframe(data=new_df)
        with placeholder.container():
            show_text = visualisation.display_text(data=new_df)
        st.sidebar.write("Nombre de textes après regroupement: ", len(new_df))
        #csv = convert_df(new_df)


        

    st.sidebar.divider()
    #st.sidebar.form("Télécharger un corpus Prospéro")
    st.sidebar.write("Créer un corpus Prospéro")
    list_col_name = [x for x in df.columns if "name" in x]
    name = st.sidebar.selectbox("auteur", list_col_name)
    narrateur = st.sidebar.selectbox("narrateur", [""])
    destinataire = st.sidebar.selectbox("destinataire", list_col_name)
    type_support = st.sidebar.selectbox("support", ("Twitter", "Twitch", "Instagram","Youtube"))
    nom_support = st.sidebar.text_input("Nom de l'émission")
    observation = st.sidebar.selectbox("observation", [x for x in df.columns])
    statut = st.sidebar.selectbox("statut", [x for x in df.columns])
    champ1 = st.sidebar.selectbox("champ 1", [x for x in df.columns])
    champ2 = st.sidebar.selectbox("champ 2", [x for x in df.columns])
    folder_path = st.sidebar.text_input("Entrer l'adresse du dossier de récupération")



    create_txt = st.sidebar.button('Télécharger un corpus Prospéro')


    if create_txt :
        #print(folder_path)
        new_df = gp.group_by_user_by_minute(df, number, minute_interval)
        new_df = new_df.loc[~(new_df["text"].isna())]

        #st.sidebar.write('You selected `%s`' % filename)
        convert_csv_to_txt = convert.ParseCsv.write_prospero_files(new_df, save_dir=folder_path, nom_support=nom_support, type_support=type_support)
        #create_prc
