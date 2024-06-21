import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import grouping_post as gp
import visualisation
import convert
import zipfile
import cleaning
from cleaning import Cleaner
import emoji
import psql_to_stream
#import streamlit as st
#from tkinter import filedialog
#import glob

# Script inspired from https://github.com/emilienschultz/dstool

# Fonction pour afficher les "topics disponibles"
def dic_emission_twit():
    dfe = pd.read_csv("data-1718699997549.csv")
    dfe = dfe[["collect_filePath"]].drop_duplicates()
    dict_emission = {}
    for n, x in enumerate(dfe.collect_filePath):
        file = dfe.collect_filePath.iloc[n]
        nom_emission = file.split('/')[-1]
        #print(nom_emission.split('.xls')[0])
        dict_emission[nom_emission.split('.xls')[0]] = x
    return dict_emission

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


@st.cache_data # évite que cette fonction soit exécutée à chaque fois
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

@st.cache_resource
def init_connection():
    return st.connection("postgresql", type="sql")


tab1, tab2, tab3 = st.tabs(["Tableau", "Texte", "label"])
with tab1 :
    placeholder = st.empty()
    container = st.container()

with tab2:
    placeholder2 = st.empty()
    container2 = st.container()
with tab3:

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
    placeholder3 = st.empty()
    container3 = st.container()


#  Chargement du CSV contenant les tweets (un seul fichier à la fois)
st.sidebar.title("Mes données d'origine")
bdd = st.sidebar.radio(
    "Je veux construire un corpus Prospéro depuis",
    ["Un fichier CSV", "Une base donnée postgresql"])

if bdd == "Un fichier CSV":
    uploaded_files = st.sidebar.file_uploader("Téléverser le fichier csv", accept_multiple_files=False)
    if uploaded_files is not None:
        dic_id={}
        list_col = [x for x in pd.read_csv(uploaded_files).columns if 'id' in x]
        for x in list_col:
            dic_id[x] = "string"

        uploaded_files.seek(0)
        df0 = pd.read_csv(uploaded_files, dtype = dic_id)
        column_author = st.sidebar.selectbox("Auteur", [x for x in df0.columns if "name" in x])
        source = st.sidebar.text_input("Nom de la source", value="Tapez le nom de la source (twitter, twitch, etc.)")
        df0 = df0.rename(columns={column_author:"author"})

        df = gp.df_processor(data=df0, source = source)


else:
    # Initialize connection.
    _conn = init_connection()
    #conn = st.connection("postgresql", type="sql", url="postgresql://Aymeric:jhsd4098ug4k3@postgres:5432/dbname")
    plateform = st.sidebar.selectbox("Quelle plateforme vous intéresse ?",
    ("Twitch", "Twitter"))
    # Perform query.
    if plateform == "Twitch":
        df0 = psql_to_stream.connect_twitch(_conn)
        df = gp.df_processor(data=df0, source = "Twitch")

    elif plateform == "Twitter":
        dic_emission = dic_emission_twit()
        nom_emission = st.sidebar.selectbox("Emissions", [x for x in dic_emission])
        show = dic_emission[nom_emission]
        print(show)
        df0 = psql_to_stream.connect_twitter(_conn, show)
        df = gp.df_processor(data=df0, source = "Twitter")

    #st.dataframe(data=df)

try:
    with tab1 :
        #st.divider()
        placeholder = st.empty()
        container = st.container()

        with placeholder.container():
            st.write("Nombre de textes: ", len(df))
            visualisation.display_dataframe(data=df)
            #timeserie = st.pyplot(fig)
            st.divider()

            ### Option pour le regoupement
            with st.sidebar.form("grouped_posts"):
                st.write("Opérer un regroupement")
                st.info("Entrez les valeurs de votre choix pour effectuer un regroupement.", icon="ℹ️")
                number = st.number_input('Nombre minimum de mot')
                minute_interval = st.number_input("Définir l'intervale de temps (en minute)",value=0) #on concatène tous les textes publiés dans cet intervale
                submit = st.form_submit_button("Regrouper les posts")



            #with st.form("create_corpus"): #permet de choisir les données du CTX
                #print("error 1")
            st.markdown("# Créer un corpus Prospéro")
            st.info("Les textes sont créés en prenant en compte les valeur de regroupement (voir \"Opérer un regroupement\"). Si les valeurs sont à zéro, aucun regroupement n\'est effectué (i.e. on crée un fichier par tweet.).\nLes fichiers sont sauvegardés dans un dossier zip", icon="ℹ️")

            name = st.selectbox("auteur", ["author"])
            #narrateur = st.selectbox("narrateur", [""])
            #destinataire = st.selectbox("destinataire", list_col_name)
            type_support = st.selectbox("support", ("Twitter", "Twitch", "Instagram","Youtube"))
            nom_support = st.text_input("Nom de l'émission", value="Tapez le nom de l'émission")
            observation = st.selectbox("observation", [x for x in df.columns])
            folder_path = st.text_input("Coller l'adresse du dossier de récupération")
            st.info("L\'adresse ci-dessus est utilisée pour créer le prc.", icon="ℹ️")


            st.markdown("## Création du corpus Prospéro")

            # Every form must have a submit button.
            submitted = st.button("Créer le corpus")

            if submitted :
                #print(df)
                new_df= df.copy()
                new_df = new_df.loc[~(new_df["text"].isna())]

                #st.sidebar.write('You selected `%s`' % filename)
                convert_csv_to_txt = convert.ParseCsv.write_prospero_files(new_df, save_dir=folder_path, nom_support=nom_support, type_support=type_support, observation= observation)
                #create_prc
                print("OK")
                st.download_button(
                    "Download corpus",
                    #on_click = zipfile_creator(),
                    file_name="corpus.zip",
                    mime="application/zip",
                    data=convert_csv_to_txt
                )
    with tab2 :
        placeholder2 = st.empty()
        container2 = st.container()
        with placeholder2.container():
            #show_text = visualisation.display_text(data=df)
            show_text = visualisation.display_text(data=df)



except:
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
try:
    with tab2 :
        placeholder2 = st.empty()
        container2 = st.container()
        with placeholder2.container():
            #show_text = visualisation.display_text(data=df)
            st.markdown(
                """
                Ca ne marche pas
                """
            )

except:
    with tab2 :
        placeholder2 = st.empty()
        container2 = st.container()
        with placeholder2.container():
            st.markdown(
                """
                Ca ne marche pas
                """
            )
