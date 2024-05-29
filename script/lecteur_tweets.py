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

# def select_folder():
#    root = tk.Tk()
#    root.withdraw()
#    folder_path = filedialog.askdirectory(master=root)
#    root.destroy()
#    return folder_path
#
# def save_csv(data):
#     root = tk.Tk()
#     root.withdraw()
#     files = [('csv', '*.csv')]
#     file = filedialog.asksaveasfile(filetypes = files, defaultextension = files)
#     #print(file)
#     #data.to_csv(file, index=False)
#     if file:
#         print(file)
#         data.to_csv(file, index=False)
#     root.destroy()
    #return file



@st.cache_data # évite que cette fonction soit exécutée à chaque fois
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun

    return df.to_csv(index=False).encode('utf-8')



#  Chargement du CSV contenant les tweets (un seul fichier à la fois)
st.sidebar.title("Chargement d'un fichier CSV")
uploaded_files = st.sidebar.file_uploader("Téléverser le fichier csv", accept_multiple_files=False)
st.sidebar.write(uploaded_files.name)
# selected_folder_path = st.session_state.get("folder_path", None)
# folder_select_button = st.sidebar.button("Dossier de récupération du corpus")
# if folder_select_button:
#     selected_folder_path = select_folder()
#     st.session_state.folder_path = selected_folder_path
#
# if selected_folder_path:
#     st.sidebar.write(selected_folder_path)

if uploaded_files is not None:
    path_in = uploaded_files.name
    print(path_in)
else:
    path_in = None




if uploaded_files is not None:
    df = gp.df_processor(uploaded_files)

    st.sidebar.write("Nombre de lignes: ", len(df))

    buildcorpus = st.sidebar.form("Opérer un regroupement")
    buildcorpus.write("Opérer un regroupement")
    number = buildcorpus.number_input('Nombre minimum de mot')
    minute_interval = buildcorpus.number_input("Définir l'intervale de temps (en minute)",value=30) #on concatène tous les textes publiés dans cet intervale
    submit = buildcorpus.form_submit_button(f'Regrouper')


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
        #buildcorpus.write("Nombre de lignes new_df: ", len(new_df))
        csv = convert_df(new_df)


        # save_corpus_in_csv = st.sidebar.button("Sauvegarder CSV")
        # if save_corpus_in_csv:
        #     selected_folder_path = save_csv(new_df)
            #st.session_state.folder_path = selected_folder_path




    downlaod_corpus = st.sidebar.form("Télécharger un corpus Prospéro")
    downlaod_corpus.write("Créer un corpus Prospéro")
    list_col_name = [x for x in df.columns if "name" in x]
    name = downlaod_corpus.selectbox("auteur", list_col_name)
    narrateur = downlaod_corpus.selectbox("narrateur", [""])
    destinataire = downlaod_corpus.selectbox("destinataire", list_col_name)
    type_support = downlaod_corpus.selectbox("support", ("Twitter", "Twitch", "Instagram","Youtube"))
    nom_support = downlaod_corpus.selectbox("Nom de l'émission", ["Face aux françaises", 'Test'])
    observation = downlaod_corpus.selectbox("observation", [x for x in df.columns])
    statut = downlaod_corpus.selectbox("statut", [x for x in df.columns])
    champ1 = downlaod_corpus.selectbox("champ 1", [x for x in df.columns])
    champ2 = downlaod_corpus.selectbox("champ 2", [x for x in df.columns])

    f_out = downlaod_corpus.text_input(label='Output Folder path: ',  value=dflt_fname)



    create_txt = downlaod_corpus.form_submit_button('Télécharger un corpus Prospéro')


    if create_txt :
        print(selected_folder_path)
        new_df = gp.group_by_user_by_minute(df, number, minute_interval)
        new_df = new_df.loc[~(new_df["text"].isna())]

        #downlaod_corpus.write('You selected `%s`' % filename)
        convert_csv_to_txt = convert.ParseCsv.write_prospero_files(new_df, save_dir=f_out)
        #create_prc
