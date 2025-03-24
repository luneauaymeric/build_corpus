import streamlit as st
import pandas as pd
import io

from datetime import datetime, timedelta


import psql_to_stream
import requests
from io import StringIO
import re
import os
import psql_builder

@st.cache_resource
def init_connection():
    return st.connection("postgresql", type="sql")




#def rebase_count():
    #st.session_state.count = 0

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
    requete = psql_builder.psql_builder(_conn=_conn)
    rebase_count()

       
    
    #st.code(st.session_state.build_requete['item'], language="sql")

if "build_requete" not in st.session_state:
    st.code("", language="sql")
else:
    st.code(st.session_state.build_requete['item'], language="sql")
    df = _conn.query(st.session_state.build_requete['item'])



