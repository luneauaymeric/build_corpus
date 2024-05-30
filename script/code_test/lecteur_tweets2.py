import streamlit as st
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import grouping_post as gp
import visualisation
import convert
import zipfile
from streamlit_text_label import Selection, label_select
import test_label as tl
import io

# Script inspired from https://github.com/emilienschultz/dstool

@st.cache_data
def get_body(data):
    text_body= data.text.iloc[14]
    #text_body = visualisation.display_text(data=df)
    return text_body


@st.cache_data # évite que cette fonction soit exécutée à chaque fois
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

@st.cache_data
def zipfile_creator(data):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        #list_file = []
        for n, text in enumerate(data.text):
            text_byte = io.BytesIO(text.encode('utf-8'))
            #list_file.append((f"data{n}.txt", text_byte))
            zip_file.writestr(f"data{n}.txt", text_byte.getvalue())
    buf = zip_buffer.getvalue()
    zip_buffer.close()
    return buf



#  Chargement du CSV contenant les tweets (un seul fichier à la fois)
st.sidebar.title("Chargement d'un fichier CSV")
uploaded_files = st.sidebar.file_uploader("Téléverser le fichier csv", accept_multiple_files=False)


if uploaded_files is not None:
    path_in = uploaded_files.name
    print(path_in)
else:
    path_in = None

dict_labeled_term={}


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

st.sidebar.write(dict_labeled_term)
st.sidebar.divider()
if uploaded_files is not None:
    df = gp.df_processor(uploaded_files)
    st.sidebar.write("Nombre de textes: ", len(df))
    fig = visualisation.tracer_graphique(data = df, d = "Jour")

    with tab1 :
        st.divider()
        placeholder = st.empty()
        container = st.container()
        with placeholder.container():
            timeserie = st.pyplot(fig)
            st.dataframe(data=df)

    with tab2:
        placeholder2 = st.empty()
        container2 = st.container()
        with placeholder2.container():
            show_text = visualisation.display_text(data=df)
    with tab3:
        placeholder3 = st.empty()
        container3 = st.container()
        with placeholder3.container():
            selected = label_select(
                body= get_body(df),
                labels= tl.get_labels(),
                #selections= tl.get_selections(),
            )
            #dic_selected = dict(selected)
            st.write(selected)

            for x in selected:
                list_select = str(x).replace("Selection(","").replace(")","").split(",")
                list_v = [v.split('=')[-1] for v in list_select]
                labeled_term = list_v[2].replace("\"","").replace("\'","")
                type_term = list_v[-1].replace("[\'","").replace("\']","")
                dict_labeled_term[labeled_term] = type_term

    st.sidebar.download_button(
        "Download corpus",
        #on_click = zipfile_creator(),
        file_name="data.zip",
        mime="application/zip",
        data=zipfile_creator(df)
    )
