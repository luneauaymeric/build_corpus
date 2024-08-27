import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

@st.cache_data
def df_processor(data, source):
    '''Fonction pour mettre en forme le fichier csv : on définit le type des colonnes, on convertit les colonnes "de date" au format Date etc.

    uploaded_files : a csv'''

    data['local_time'] = pd.to_datetime(pd.to_datetime(data['local_time']))

    data['date'] = pd.to_datetime(pd.to_datetime(data['local_time']).dt.date)

    data['yearmonth']=(data['date'].dt.strftime('%Y-%m'))
    data["yearmonth"] = pd.to_datetime(data.yearmonth, format='%Y-%m')

    #On compte le nombre de mot pour ensuite filtrer les texts en fonction de leur longueur
    data["length_text"] = data.text.str.len()
    data["split_txt"] = data.text.str.split(" ")
    data["nb_word"]= data.split_txt.str.len()

    if "retweeted_id" in data.columns:
        data = data.loc[(data["retweeted_id"].isna())]
        data = data.reset_index()
        data = data.drop(columns=["index"])
    else:
        pass


    data["year"]= data.local_time.dt.year
    data["month"]= data.local_time.dt.month
    data["day"]= data.local_time.dt.day
    data["hour"]= data.local_time.dt.time
    #dg["date"] = dg.local_time.dt.date
    data["source"] = source

    data = data.sort_values("local_time",ascending=True).reset_index().drop(columns=["index"])


    return data

def group_by_user_by_minute(data, number, minute_interval):

    data = data.loc[data["nb_word"]>=number]
    list_user =[]
    list_text=[]
    list_min_date=[]
    list_max_date=[]
    for n, user in enumerate(data.author.unique()):
        print(user)
        dtemp = data.loc[data["author"]==user]
        dtemp = dtemp.drop_duplicates(subset="text")
        n_row = len(dtemp)
        compteur = 0
        while compteur < n_row:
            first_tweet = dtemp.local_time.min()
            dtemp1 = dtemp.loc[(dtemp["local_time"] >= first_tweet) &
                               (dtemp["local_time"]<= first_tweet+timedelta(minutes = int(minute_interval)))]
            min_date = dtemp1.local_time.min()
            max_date = dtemp1.local_time.max()
            for m, tweets in enumerate(dtemp1.text):
                if m == 0:
                    concat_text = tweets
                else:
                    concat_text = f"{concat_text}\n.\n\n{tweets}"
            concat_text = concat_text.replace('«\xa0', '\"')
            concat_text = concat_text.replace('\xa0»', '\"')
            concat_text = concat_text.replace("’", "\'")
            list_user.append(user)
            list_text.append(concat_text)
            list_min_date.append(min_date)
            list_max_date.append(max_date)
            dtemp = dtemp.loc[(dtemp["local_time"]>= first_tweet+timedelta(minutes = int(minute_interval)))]
            compteur += len(dtemp1)

    dict_data = {"author": list_user, "text":list_text, "min_date": list_min_date, "max_date":list_max_date}
    dg = pd.DataFrame(dict_data)
    dg["year"]= dg.min_date.dt.year
    dg["month"]= dg.min_date.dt.month
    dg["day"]= dg.min_date.dt.day
    dg["hour"]= dg.min_date.dt.time
    dg["date"] = dg.min_date.dt.date
    dg["source"] = "Twitter"
    dg = dg.merge(data[["author"]].drop_duplicates(), on = ["author"], how = "left")

    return dg
