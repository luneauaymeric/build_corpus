import streamlit as st
import pandas as pd
import io
from io import StringIO

from datetime import datetime, timedelta


import psql_to_stream
import emission_dictionary as ed
import requests
import re


def rebase_count():
    st.session_state.count = 0

def type_of_column(data, filtre, plateform, table, _conn):

    if filtre == "emissions":
        dfe = ed.read_dfemission()
        print(dfe.columns)
        if plateform == "twitch":
            dfet = dfe.loc[~dfe["twitch_id"].isna()]
            print(dfet.columns)
            print('len dfet : ', len(dfet))
            dict_emission = dict(zip(dfet.twitch_id, dfet["Publication Title"]))

            list_emission = list(dict.fromkeys([dict_emission[x] for x in dict_emission]))
            search_in_column = st.multiselect("Select a value", list_emission)
            operator = st.radio("Select an operator: ", options=["contains", "does not contain"])
            id_emission = [x for x in dfet.twitch_id.loc[dfet["Publication Title"].isin(search_in_column)]]
            if operator == "contains":
                search_phrase = f"SELECT * FROM public.twitch_comment t JOIN public.person ta ON t.person_id = ta.id WHERE t.pub_reference_id IN {tuple(id_emission)}"
            elif operator == "does not contain":
                search_phrase = f"SELECT * FROM public.twitch_comment t JOIN public.person ta ON t.person_id = ta.id WHERE t.pub_reference_id NOT IN {tuple(id_emission)}"

        elif plateform == "youtube":
            dfy = dfe.loc[~dfe["list_youtube_id"].isna()]

            dfy["youtube_id"] = dfy["list_youtube_id"].str.split("|")
            dfyxplode = dfy.explode("youtube_id")

            dict_emission = dict(zip(dfyxplode.youtube_id, dfyxplode["Publication Title"]))

            list_emission = list(dict.fromkeys([dict_emission[x] for x in dict_emission]))

            search_in_column = st.multiselect("Select a value", list_emission)
            operator = st.radio("Select an operator: ", options=["contains", "does not contain"])

            id_emission = [x for x in dfyxplode.youtube_id.loc[dfyxplode["Publication Title"].isin(search_in_column)]]
            if operator == "contains":
                search_phrase = f"SELECT * FROM public.youtube_comment t JOIN public.youtube_account ta ON t.person_id = ta.person_id WHERE t.publication_id IN {tuple(id_emission)}"

            elif operator == "does not contain":
                search_phrase = f"SELECT * FROM public.youtube_comment t JOIN public.youtube_account ta ON t.person_id = ta.person_id WHERE t.publication_id NOT IN {tuple(id_emission)}"




    
    elif data.data_type.loc[data["column_name"]==filtre].iloc[0] == "integer":
        search_in_column = st.number_input("Insert a number")
        operator = st.radio("Select an operator: ", options=["equal", "superior to", "inferior to"])
        if operator == "equal":
            search_phrase = f'SELECT * FROM public.\"{table[plateform]}\" WHERE \"{filtre}\" = {search_in_column}'
        elif operator == "superior to":
            search_phrase = f'SELECT * FROM public.\"{table[plateform]}\" WHERE \"{filtre}\" > {search_in_column}'
        elif operator == "inferior to":
            search_phrase = f'SELECT * FROM public.\"{table[plateform]}\" WHERE \"{filtre}\" < {search_in_column}'

    else:
        if data.data_type.loc[data["column_name"]==filtre].iloc[0] == 'text':
            search_in_column = st.text_input("What are you looking for (if you are looking for several keywords, separate them by a comma (e.g. cancer, tumor))")
            key_search = search_in_column.replace("  ", " ").split(",")
            pattern_hash="|".join(key_search).lower().replace(" |", " |").replace("| ", "|")
            st.write(pattern_hash)
            operator = st.radio("Select an operator: ", options=["contains", "does not contain"])
            if operator == "contains":
                if plateform == "twitter":
                    search_phrase = f"SELECT * FROM public.\"{table[plateform]}\" WHERE LOWER({filtre}) SIMILAR TO \'%({pattern_hash})%\' AND pub_date > \'1971-01-02\'"
                else:
                    search_phrase = f"SELECT * FROM public.\"{table[plateform]}\" WHERE LOWER({filtre}) SIMILAR TO \'%({pattern_hash})%\'"
            elif operator == "does not contain":
                if plateform == "twitter":
                    search_phrase = f"SELECT * FROM public.\"{table[plateform]}\" WHERE LOWER({filtre}) NOT SIMILAR TO \'%({pattern_hash})%\' AND pub_date > \'1971-01-02\'"
                else:
                    search_phrase = f"SELECT * FROM public.\"{table[plateform]}\" WHERE LOWER({filtre}) NOT SIMILAR TO \'%({pattern_hash})%\' AND pub_date"


        elif filtre == "local_time" or filtre == "date":
            start_date = st.date_input("Start of the period", value = "2020-01-01", min_value = "2020-01-01", max_value="2022-12-31")
            end_date = st.date_input("End of the period", value = "2022-12-31", min_value = "2020-01-01", max_value="2022-12-31")
            search_in_column = [start_date, end_date]

        else:
            df = _conn.query(f'SELECT DISTINCT \"{filtre}\" FROM public.\"{table[plateform]}\"', ttl="10m")
            search_in_column = st.multiselect("Select a value", [x for x in df[f'{filtre}'].unique()])
            operator = st.radio("Select an operator: ", options=["similar to", "differnt from"])
    return search_phrase

        



@st.dialog("Construisez votre requête")
def psql_builder(_conn):

    on = st.toggle("I don't need help to build my request")

    if on:
        search_phrase = st.text_input("Write your request")
        if st.button("Submit"):
            get_platefom = re.search('youtube|twitch|twitter|instagram', search_phrase)

            st.session_state.build_requete = {"item": search_phrase, "plateform":get_platefom.group(0)}
            st.rerun()
        

    else:
        plateform = st.selectbox("Choix de la plateforme", ("twitch", "twitter","youtube", "instagram"), index = None, on_change=rebase_count)

        table_corpus={"twitch": "twitch_comment", "twitter":"twitter_post","youtube":"youtube_comment", "instagram":"instagram_comment"}

        if plateform:
            rows = _conn.query(f'select * from information_schema.columns WHERE table_schema = \'public\' and table_name=\'{table_corpus[plateform]}\'', ttl="10m")
            df = _conn.query(f'select * from public.\"{table_corpus[plateform]}\" LIMIT 5 ', ttl="10m")
            st.write(len(df))
            list_columns = [x for x in rows.column_name]
            if plateform == "twitch" or plateform=="youtube":
                list_columns.append("emissions")
            else:
                pass

            variable = st.selectbox("Choix de la variable", list_columns, index = None)
            if variable:
                st.write(variable)
                #st.write("TYPE : ", rows.data_type.loc[rows["column_name"]==variable].iloc[0])
                value = type_of_column(rows, variable, plateform, table_corpus, _conn=_conn)
                
            
            if st.button("Submit"):
                st.session_state.build_requete = {"item": value, "plateform": plateform}
                st.rerun()

