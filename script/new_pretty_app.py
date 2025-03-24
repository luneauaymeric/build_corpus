
import os
import requests

import io
from io import StringIO

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime, timedelta
import re

import zipfile
import emoji




## intern module (module construit pour l'application)
import emission_dictionary

import grouping_post as gp
import visualisation
import convert

import cleaning
from cleaning import Cleaner

import psql_builder
import psql_to_stream


###########

def next_quote(df):
    print("next : ", st.session_state.count)
    if st.session_state.count + 1 >= len(df):
        st.session_state.count = 0
    else:
        st.session_state.count += 1

def previous_quote():
    print("previous : ", st.session_state.count)
    if st.session_state.count > 0:
        st.session_state.count = st.session_state.count - 1
    else:
        pass

def first_quote():
    print("previous : ", st.session_state.count)
    if st.session_state.count > 0:
        st.session_state.count = 0
    else:
        pass

def last_quote(df):
    print("next : ", st.session_state.count)
    if st.session_state.count + 1 >= len(df):
        st.session_state.count = 0
    else:
        st.session_state.count = len(df) - 1








def topics(data,topic_column):
    d_topic = data.groupby([topic_column]).agg(nb = ("id", "size")).sort_values("nb", ascending=False).reset_index()
    list_topics = [x for x in d_topic[topic_column].unique()]
    return list_topics



def download_corpus(df):
    df1 = pd.DataFrame(df)
    print("OK", type(df1))
    components.html(
        download_button(object_to_download=df1, download_filename="corpus.csv"),
        height=0,
    )




@st.cache_data
def read_dfemission():
    current_directory = os.getcwd()
    print(current_directory)
    if 'aymeric' in current_directory:
        return   pd.read_csv("liste_emission.csv", sep = ",")
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    else:
        return   pd.read_csv("./script/liste_emission.csv", sep = ",")


@st.cache_data
def read_markdown_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        txt = StringIO(response.text).read()
        print("TXT : ", txt)
        return txt
        #return pd.read_csv(StringIO(response.text))
    else:
        return st.error("Failed to load data from GitHub.")



@st.cache_data # évite que cette fonction soit exécutée à chaque fois
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

@st.cache_resource
def init_connection():
    return st.connection("postgresql", type="sql")




if 'count' not in st.session_state:
    st.session_state.count = 0

### Front hand

tab0, tab1, tab3 = st.tabs(["Read Me","Tableau", "Texte par texte", ])
with tab0:
    url = "https://raw.githubusercontent.com/luneauaymeric/build_corpus/main/README.md"
    readme_text = read_markdown_file(url=url)
    placeholder0 = st.empty()
    container0 = st.container()
    with placeholder0.container():
        #show_text = visualisation.display_text(data=df)
        st.markdown(readme_text)

with tab1 :
    placeholder = st.empty()
    container = st.container()


with tab3:

    placeholder3 = st.empty()
    container3 = st.container()



#  Chargement du CSV contenant les tweets (un seul fichier à la fois)
st.session_state.result_requests = 0
st.session_state.corpus = False
st.sidebar.title("Mes données d'origine")
bdd = st.sidebar.radio(
    "Je veux construire un corpus Prospéro depuis",
    ["Un fichier CSV", "Une base donnée postgresql"])

if bdd == "Un fichier CSV":
    st.session_state.bdd = "CSV"
    uploaded_files = st.sidebar.file_uploader("Téléverser le fichier csv", accept_multiple_files=False)
    if uploaded_files is not None:
        dic_id={}
        list_col = [x for x in pd.read_csv(uploaded_files).columns if 'id' in x]
        for x in list_col:
            dic_id[x] = "string"

        uploaded_files.seek(0)
        df0 = pd.read_csv(uploaded_files, dtype = dic_id)

        st.sidebar.divider()
        column_author = st.sidebar.selectbox("Auteur", [x for x in df0.columns if "name" in x])
        source = st.sidebar.text_input("Nom de la source", value="Tapez le nom de la source (twitter, twitch, etc.)")
        df0 = df0.rename(columns={column_author:"author"})

        df = gp.df_processor(data=df0, source = source)
        st.session_state.result_requests = 1
        st.session_state.dataframe = df





else:
    st.session_state.bdd = "PSQL"


    dfe = read_dfemission()

    _conn = init_connection()

    if st.sidebar.button("construire une requête"):
        #_conn = init_connection()
        requete = psql_builder.psql_builder(_conn=_conn)
        psql_builder.rebase_count()

       
    
    #st.code(st.session_state.build_requete['item'], language="sql")

    if "build_requete" in st.session_state:
        df = psql_to_stream.connect_amulex(_conn, search_phrase = st.session_state.build_requete['item'], plateform = st.session_state.build_requete['plateform'])
        
        st.session_state.requete = True





if st.session_state.result_requests == 1:



    st.sidebar.divider()
    st.sidebar.markdown("## Regrouper les posts")
    st.sidebar.info("Entrez les valeurs de votre choix pour effectuer un regroupement.", icon="ℹ️")
    number = st.sidebar.number_input('Nombre minimum de mot', key = "nombre_mot" )
    minute_interval = st.sidebar.number_input("Définir l'intervale de temps (en minute)",value=0, key ="nombre_minute") #on concatène tous les textes publiés dans cet intervale

    if st.session_state.nombre_mot > 0 or st.session_state.nombre_minute > 0:
        new_df = st.session_state.dataframe.loc[~(st.session_state.dataframe["text"].isna())]
        if number+minute_interval>0:
            df = gp.group_by_user_by_minute(new_df, number, minute_interval)
            print(new_df.columns)
        else:
            pass



    st.sidebar.divider()

    ### Option pour le regoupement

   

    name = st.sidebar.selectbox("auteur", ["author"])

    observation = st.sidebar.selectbox("observation", [x for x in st.session_state.dataframe.columns])
    folder_path = st.sidebar.text_input("Coller l'adresse du dossier de récupération")
    dictionnary_path = st.sidebar.text_input("Coller l'adresse des dictionnaires")
    st.sidebar.info("L\'adresse ci-dessus est utilisée pour créer le prc.", icon="ℹ️")

    submit = st.sidebar.button("Créer le corpus")
    if submit :

        convert_csv_to_txt = convert.ParseCsv.write_prospero_files(df, save_dir=folder_path, observation= observation)
   
        st.sidebar.download_button(
            "Download corpus",
            #on_click = zipfile_creator(),
            file_name="corpus.zip",
            mime="application/zip",
            data=convert_csv_to_txt
        )




    with tab1 :
        #st.divider()
        placeholder = st.empty()
        container = st.container()

        with placeholder.container():

            
            st.code(st.session_state.build_requete['item'], language="sql")
            st.divider()
            df = st.session_state.dataframe.drop_duplicates(subset=["author", "text", "date"])
            st.write("Nombre de textes: ", len(df))
            print(df.columns)
            visualisation.display_dataframe(data=df)
            #fig = visualisation.tracer_graphique(data=df, d = "Jour")
            #timeserie = st.pyplot(fig)

                #st.session_state.corpus = True






    with tab3 :
        placeholder3 = st.empty()
        container3 = st.container()
        with placeholder3.container():
            visualisation.display_quote1(st.session_state.dataframe)
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if st.button("⏮️ ⏮️ First"):
                    first_quote()
                else:
                    pass

            with col2:
                if st.button("⏮️ Previous"):
                    previous_quote()
                else:
                    pass

            with col3:
                if st.button("Next ⏭️"):
                    next_quote(df)
                else:
                    pass

            with col4:
                if st.button("Last ⏭️ ⏭️"):
                    last_quote(df)
                else:
                    pass



elif st.session_state.result_requests == 0 :
    with tab1 :
        placeholder = st.empty()
        container = st.container()
        with placeholder.container():
            st.header("Aucun CSV")
            st.markdown(
                """
                Si vous voulez construire un corpus pour Prospéro, chargez un fichier ou connectez-vous à la base de données.
                Le CSV doit avoir les 3 colonnes suivantes (l'ordre n'a pas d'importance):

                |Author | Text | Date |
                |-------|------|------|
                | X     | lllll| YYYY-MM-DD|
                """
            )

    with tab3:

        placeholder3 = st.empty()
        container3 = st.container()
        with placeholder3.container():
            st.header("Label selected text")
            st.markdown(
                """
                To add a new annotation

                1. Pick a label
                2. Highlight text with cursor

                To delete an annotation

                1. Click highlighted text
                2. Press backspace

                Finally, click `Update` to propagate changes to streamlit.
                """
            )

elif st.session_state.result_requests == -1 :
    with tab1 :
        placeholder = st.empty()
        container = st.container()
        with placeholder.container():
            st.header("0 publication")
            st.markdown(
                """
                Aucune publication ne correspond aux éléments de la requête. Essayez une autre émission ou d'autre.s candidat.es
                """
            )

    with tab3:

        placeholder3 = st.empty()
        container3 = st.container()
        with placeholder3.container():
            st.header("0 publication")
            st.markdown(
                """
                Aucune publication ne correspond aux éléments de la requête. Essayez une autre émission ou d'autre.s candidat.es
                """
            )
