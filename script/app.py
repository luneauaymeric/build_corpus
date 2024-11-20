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
import requests
from io import StringIO
import re
#import streamlit as st
#from tkinter import filedialog
#import glob

# Script inspired from https://github.com/emilienschultz/dstool


### Définition des fonctions


# def display_quote():
#     quote = st.session_state.quotes[st.session_state.count]
#     st.write(quote)

# def display_quote_df(df):
#     quote = df.text.iloc[st.session_state.count]
#     st.write(quote)

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


# Fonction pour afficher les "topics disponibles"
def dic_emission_twit():
    # dfe = pd.read_csv("data-1718699997549.csv")
    # dfe = dfe[["collect_filePath"]].drop_duplicates()
    # dict_emission = {}
    # for n, x in enumerate(dfe.collect_filePath):
    #     file = dfe.collect_filePath.iloc[n]
    #     nom_emission = file.split('/')[-1]
    #     #print(nom_emission.split('.xls')[0])
    #     dict_emission[nom_emission.split('.xls')[0]] = x
    dict_emission = {'2022-04-12-lepen-tf1': 'files/twitter/lePen/2022-04-12-lepen-tf1.xlsx',
 '2022-03-24-zemmour': 'files/twitter/zemmour/2022-03-24-zemmour.xlsx',
 '2022-03-23-roussel': 'files/twitter/roussel/2022-03-23-roussel.xlsx',
 '2022-04-06-melenchon': 'files/twitter/melenchon/2022-04-06-melenchon.xlsx',
 '2022-03-23-pecresse': 'files/twitter/pecresse/2022-03-23-pecresse.xlsx',
 '2022-04-01-lassalle': 'files/twitter/lassalle/2022-04-01-lassalle.xlsx',
 '2022-04-15-lepen': 'files/twitter/lePen/2022-04-15-lepen.xlsx',
 '2022-02-15-pecresse': 'files/twitter/pecresse/2022-02-15-pecresse.xlsx',
 '2022-03-07-faceauxfrancaises': 'files/twitter/2022-03-07-faceauxfrancaises.xlsx',
 '2022-03-28-grandoral': 'files/twitter/2022-03-28-grandoral.xlsx',
 '#zemmourvsmelenchon-#faceababa-2022-01-27': 'files/twitter/#zemmourvsmelenchon-#faceababa-2022-01-27.xlsx',
 '2022-03-24-elysee': 'files/twitter/2022-03-24-elysee.xlsx',
 'tweets': 'files/twitter/roussel/tweets.xlsx',
 '2022-04-04-zemmour': 'files/twitter/zemmour/2022-04-04-zemmour.xlsx',
 '2022-04-03-poutou10mn': 'files/twitter/poutou/2022-04-03-poutou10mn.xlsx',
 '2022-04-06-lepen': 'files/twitter/lePen/2022-04-06-lepen.xlsx',
 '2022-04-07-dupont-aignan': 'files/twitter/dupontAignan/2022-04-07-dupont-aignan.xlsx',
 '2022-03-24-melenchon': 'files/twitter/melenchon/2022-03-24-melenchon.xlsx',
 '2022-03-21-roussel': 'files/twitter/roussel/2022-03-21-roussel.xlsx',
 '2022-04-06-zemmour': 'files/twitter/zemmour/2022-04-06-zemmour.xlsx',
 '2022-04-08-pecresse-tf1': 'files/twitter/pecresse/2022-04-08-pecresse-tf1.xlsx',
 '2022-03-03-lepen': 'files/twitter/lePen/2022-03-03-lepen.xlsx',
 '2022-04-13-macron': 'files/twitter/macron/2022-04-13-macron.xlsx',
 '2022-02-20-zemmour': 'files/twitter/zemmour/2022-02-20-zemmour.xlsx',
 '2022-03-31-dupont-aignan': 'files/twitter/dupontAignan/2022-03-31-dupont-aignan.xlsx',
 '2022-02-17-jadot': 'files/twitter/jadot/2022-02-17-jadot.xlsx',
 '2022-02-20-lepen': 'files/twitter/lePen/2022-02-20-lepen.xlsx',
 '2022-03-29-comptearebours': 'files/twitter/2022-03-29-comptearebours.xlsx',
 '2022-04-04-jadot': 'files/twitter/jadot/2022-04-04-jadot.xlsx',
 '2022-03-25-melenchon': 'files/twitter/melenchon/2022-03-25-melenchon.xlsx',
 '2022-03-17-jadot': 'files/twitter/jadot/2022-03-17-jadot.xlsx',
 '2022-04-06-macron': 'files/twitter/macron/2022-04-06-macron.xlsx',
 '2022-04-03-poutou': 'files/twitter/poutou/2022-04-03-poutou.xlsx',
 '2022-04-18-lepen': 'files/twitter/lePen/2022-04-18-lepen.xlsx',
 '2022-03-22-jadot': 'files/twitter/jadot/2022-03-22-jadot.xlsx',
 '2022-02-22-pecresse': 'files/twitter/pecresse/2022-02-22-pecresse.xlsx',
 '2022-03-16-pecresse': 'files/twitter/pecresse/2022-03-16-pecresse.xlsx'}


    return dict_emission




def dic_emission_twitch():
    url = 'https://raw.githubusercontent.com/luneauaymeric/build_corpus/main/script/liste_emission.csv'
    response = requests.get(url)
    if response.status_code == 200:
        dfe = pd.read_csv(StringIO(response.text))
        dict_emission = dict(zip(dfe.emission_title, dfe.twitch_id))
        return dict_emission
        #return pd.read_csv(StringIO(response.text))
    else:
        st.error("Failed to load data from GitHub.")
        return None

def dic_emission(dfe):
    #dfe = pd.read_csv("liste_emission.csv")
    dict_emission = dict(zip(dfe.emission_title, dfe.twitch_id))
    dfc= dfe[["Publication Title"]].drop_duplicates()
    list_channel = [x for x in dfc["Publication Title"]]
    dfg = dfe[["Guest"]].drop_duplicates()
    dfg["Guest2"] = dfg["Guest"].str.split(";")
    dfg = dfg["Guest2"].explode()
    list_candidat = []
    for x in dfg.drop_duplicates():
        x_nom = x.split(",")[0].strip()
        if x_nom not in list_candidat:
            list_candidat.append(x_nom)

    return dict_emission, list_candidat, list_channel


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
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return   pd.read_csv("liste_emission.csv", sep = ",")


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


def rebase_count():
    st.session_state.count = 0

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
st.session_state.dataframe = 0
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
        st.session_state.dataframe = 1





else:
    st.session_state.bdd = "PSQL"


    dfe = read_dfemission()

    st.sidebar.divider()
    dic_emission, list_candidat, list_channel = dic_emission(dfe)
    st.sidebar.markdown("## Requête vers la base de données")
    st.sidebar.info("Les variables ci-dessous permettent d'obtenir un tableau correspondant aux options choisies.", icon="ℹ️")
    plateform = st.sidebar.selectbox("Choix de la plateforme", ("Twitch", "Twitter","Youtube"), on_change=rebase_count)
    #platform2 = st.multiselect("Quelle plateforme vous intéresse ?", ["Twitch", "Twitter", "Youtube"])
    #nom_emission2 = st.selectbox("Quelle(s) émission(s)", [x for x in dic_emission])
    nom_emission3 = st.sidebar.multiselect("Choix de la ou des émission(s)", [x for x in list_channel],on_change=rebase_count)
    nom_candidat = st.sidebar.multiselect("Choix d'un.e ou de plusieurs candidat.es", [x for x in list_candidat], on_change=rebase_count)
    #ask_bdd = st.sidebar.button("Envoyer la requête")


    #if ask_bdd :
        # Initialize connection.


    if len(nom_emission3 )> 0:
        dfe = dfe.loc[dfe["Publication Title"].isin(nom_emission3)]
    else:
        pass
    print(len(nom_candidat))
    if len(nom_candidat)== 1:
        dfe = dfe.loc[dfe["Guest"].str.contains(nom_candidat[0], na=False)]
    elif len(nom_candidat)> 1:
        dfe = dfe.loc[dfe["Guest"].str.contains('|'.join(nom_candidat), na=False)]
    else:
        pass

    

    liste_hashtag = []
    for x in dfe.hashtag.loc[~dfe.hashtag.isna()]:
        split_hash = x.split("|")
        for hash in split_hash:
            if hash not in liste_hashtag:
                liste_hashtag.append(hash)
            else:
                pass
    print(liste_hashtag)

    _conn = init_connection()


    #plateform = st.sidebar.selectbox("Quelle(s) plateforme(s) vous intéresse ?",("Twitch", "Twitter", "Youtube"))

# Perform query.
    if plateform == "Twitch":
        list_publi_id = [x for x in dfe.twitch_id.loc[~dfe["twitch_id"].isna()]]
        print(list_publi_id)
        df0 = psql_to_stream.connect_twitch(_conn, list_publi_id)
        if len(df0) > 0:
            df = gp.df_processor(data=df0, source = "Twitch")
            dict_channel = dict(zip(dfe.twitch_id, dfe["Publication Title"]))
            df["twitch_id"] = df.twitch_id.astype("str")
            df = df.merge(dfe[["twitch_id", "Guest", "Publication Title"]], on = ["twitch_id"], how="left")
            nb_row = len(df)
        else:
            nb_row= 0


    elif plateform == "Youtube":
        dfe = dfe.loc[~dfe["list_youtube_id"].isna()]
        dfe["list_youtube_id"] = dfe["list_youtube_id"].str.split("|")
        dfexplode = dfe.explode("list_youtube_id")
        list_publi_id = [x for x in dfexplode.list_youtube_id]

        print('dfeexplode', len(dfexplode), dfexplode.columns)
        
        
        df0 = psql_to_stream.connect_youtube(_conn, list_publi_id)
        if len(df0) > 0:
            df = gp.df_processor(data=df0, source = "Youtube")
            #df = df.merge(dfe[["twitch_id", "Guest", "Publication Title"]], on = ["twitch_id"], how="left")
            nb_row = len(df)
            print(df.columns)
            df["publication_id"] = df.publication_id.astype("str")
            df = df.merge(dfexplode[["list_youtube_id", "Publication Title", "Publisher", "Guest"]].rename(columns={"list_youtube_id":"publication_id"}), on = ["publication_id"], how='left')
        else:
            nb_row= 0
        



    elif plateform == "Twitter":
        df0 = psql_to_stream.connect_twitter(_conn, liste_hashtag)
        if len(df0) > 0:
            df = gp.df_processor(data=df0, source = "Twitter")
            nb_row = len(df)
        else:
            nb_row= 0

    elif plateform == "Instagram":
        df0 = psql_to_stream.connect_instagram(_conn, liste_hashtag)
        if len(df0) > 0:
            df = gp.df_processor(data=df0, source = "Instagram")
            nb_row = len(df)
        else:
            nb_row= 0

    st.session_state.requete = True
    if nb_row > 0 :
        st.session_state.dataframe = 1
    elif nb_row == 0:
        st.session_state.dataframe = -1



#st.sidebar.write(st.session_state)






if st.session_state.dataframe == 1:

    #if 'quotes' not in st.session_state:
        #st.session_state.quotes = [x for x in df.text]

    st.sidebar.divider()
    st.sidebar.markdown("## Regrouper les posts")
    st.sidebar.info("Entrez les valeurs de votre choix pour effectuer un regroupement.", icon="ℹ️")
    number = st.sidebar.number_input('Nombre minimum de mot', key = "nombre_mot" )
    minute_interval = st.sidebar.number_input("Définir l'intervale de temps (en minute)",value=0, key ="nombre_minute") #on concatène tous les textes publiés dans cet intervale

    if st.session_state.nombre_mot > 0 or st.session_state.nombre_minute > 0:
        new_df = df.loc[~(df["text"].isna())]
        if number+minute_interval>0:
            df = gp.group_by_user_by_minute(new_df, number, minute_interval)
            print(new_df.columns)
        else:
            pass



    #new_df= df.copy()
    #new_df = new_df.loc[~(new_df["text"].isna())]

    #st.sidebar.write('You selected `%s`' % filename)

    st.sidebar.divider()

    ### Option pour le regoupement

    #submit = st.form_submit_button("Regrouper les posts")


    name = st.sidebar.selectbox("auteur", ["author"])
    #narrateur = st.selectbox("narrateur", [""])
    #destinataire = st.selectbox("destinataire", list_col_name)

    #nom_support = st.text_input("Nom de l'émission", value="Tapez le nom de l'émission")
    observation = st.sidebar.selectbox("observation", [x for x in df.columns])
    folder_path = st.sidebar.text_input("Coller l'adresse du dossier de récupération")
    st.sidebar.info("L\'adresse ci-dessus est utilisée pour créer le prc.", icon="ℹ️")

    submit = st.sidebar.button("Créer le corpus")
    if submit :

        convert_csv_to_txt = convert.ParseCsv.write_prospero_files(df, save_dir=folder_path, observation= observation)
        #create_prc
        #print("OK", plateform)
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
            df = df.drop_duplicates(subset=["author", "text", "date"])
            st.write("Nombre de textes: ", len(df))
            visualisation.display_dataframe(data=df)
            fig = visualisation.tracer_graphique(data=df, d = "Jour")
            timeserie = st.pyplot(fig)

                #st.session_state.corpus = True





    # with tab2 :
    #     placeholder2 = st.empty()
    #     container2 = st.container()
    #     with placeholder2.container():
    #         #show_text = visualisation.display_text(data=df)
    #         show_text = visualisation.display_text(data=df)

    with tab3 :
        placeholder3 = st.empty()
        container3 = st.container()
        with placeholder3.container():
            #show_text = visualisation.display_text(data=df)
            visualisation.display_quote1(df)
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



elif st.session_state.dataframe == 0 :
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

elif st.session_state.dataframe == -1 :
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
