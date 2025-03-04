import streamlit as st
import pandas as pd
import io

from datetime import datetime, timedelta


import psql_to_stream
import requests
from io import StringIO
import re
import os


@st.dialog("Construisez votre requête")
def psql_builder(_conn):
    plateform = st.selectbox("Choix de la plateforme", ("Twitch", "Twitter","Youtube", "Instagram"), index = None, on_change=rebase_count)

    table_corpus={"Twitch": "twitch_comment", "Twitter":"twitter_post","Youtube":"youtube_comment", "Instagram":"instagram_comment"}

    if plateform:

        rows = _conn.query(f'select * from information_schema.columns WHERE table_schema = \'public\' and table_name=\'{table_corpus[plateform]}\'', ttl="10m")
        list_columns = [x for x in rows.column_name]
        variable = st.selectbox("Choix de la variable", list_columns, index = None)
        code = f'''SELECT * FROM public.twitch_comment WHERE {variable}'''
        
        if st.button("Submit"):
            st.session_state.build_requete = {"item": code}
            st.rerun()


@st.cache_resource
def init_connection():
    return st.connection("postgresql", type="sql")




def rebase_count():
    st.session_state.count = 0

if 'count' not in st.session_state:
    st.session_state.count = 0

### Front hand


st.session_state.bdd = "PSQL"

st.sidebar.divider()
st.sidebar.markdown("## Requête vers la base de données")
st.sidebar.info("Les variables ci-dessous permettent d'obtenir un tableau correspondant aux options choisies.", icon="ℹ️")




_conn = init_connection()


if st.sidebar.button("construire une requête"):
    _conn = init_connection()
    requete = psql_builder(_conn=_conn)
       
    
    #st.code(st.session_state.build_requete['item'], language="sql")

if "build_requete" not in st.session_state:
    st.code("", language="sql")
else:
    st.code(st.session_state.build_requete['item'], language="sql")



