import os
import requests
import pandas as pd
import streamlit as st
from io import StringIO


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

@st.cache_data
def read_dfemission():
    current_directory = os.getcwd()
    print(current_directory)
    if 'aymeric' in current_directory:
        return   pd.read_csv("liste_emission.csv", sep = ",")
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    else:
        return   pd.read_csv("./script/liste_emission.csv", sep = ",")