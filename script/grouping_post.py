import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

@st.cache_data
def df_processor(uploaded_files):
    '''Fonction pour mettre en forme le fichier csv : on définit le type des colonnes, on convertit les colonnes "de date" au format Date etc.

    uploaded_files : a csv'''

    dic_id={}
    for x in [x for x in pd.read_csv(uploaded_files).columns if 'id' in x]:
        dic_id[x]=str

    uploaded_files.seek(0)
    df0 = pd.read_csv(uploaded_files, dtype = dic_id)
    df0['local_time'] = pd.to_datetime(pd.to_datetime(df0['local_time']))

    df0['date'] = pd.to_datetime(pd.to_datetime(df0['local_time']).dt.date)
    #df0['date'] = pd.to_datetime(pd.to_datetime(df0['local_time']).dt.strftime.date)

    #df0['Year'] = df0['date'].dt.year
    #df0['date'] = pd.to_datetime(df0['date'], format='%Y-%m-%d')
    df0['yearmonth']=(df0['date'].dt.strftime('%Y-%m'))
    df0['year']=(df0['date'].dt.strftime('%Y'))
    df0["year"] = pd.to_datetime(df0.year, format='%Y')
    df0["yearmonth"] = pd.to_datetime(df0.yearmonth, format='%Y-%m')

    #On compte le nombre de mot pour ensuite filtrer les texts en fonction de leur longueur
    df0["length_text"] = df0.text.str.len()
    df0["split_txt"] = df0.text.str.split(" ")
    df0["nb_word"]= df0.split_txt.str.len()

    #dfo = df0.loc[(df0["retweeted_id"].isna()) & (df0["nb_word"]>10)].reset_index() #on pourra choisir le seuil de mot
    dfo = df0.loc[(df0["retweeted_id"].isna())]#.reset_index() #on pourra choisir le seuil de mot
    dfo1 = dfo.groupby(["user_id"]).agg(nb_text_user:("text","size")).reset_index()
    dict_nb_text = dict(zip(dfo1.user_id, dfo1.nb_text_user))
    dfo["nb_text_user"]= dfo.user_id.map(dict_nb_text.get)
    dfo = dfo.loc[(dfo["nb_text_user"]>1)].reset_index()
    dfo = dfo.drop(columns=["index"])
    dfo["year"]= dfo.local_time.dt.year
    dfo["month"]= dfo.local_time.dt.month
    dfo["day"]= dfo.local_time.dt.day
    dfo["hour"]= dfo.local_time.dt.time
    #dg["date"] = dg.local_time.dt.date
    dfo["source"] = "Twitter"


    return dfo

def group_by_user_by_minute(data, number, minute_interval):

    data = data.loc[data["nb_word"]>=number]
    list_user =[]
    list_text=[]
    list_min_date=[]
    list_max_date=[]
    for n, user in enumerate(data.user_screen_name.unique()):
        print(user)
        dtemp = data.loc[data["user_screen_name"]==user]
        dtemp = dtemp.drop_duplicates(subset="text")
        n_row = len(dtemp)
        compteur = 0
        while compteur < n_row:
            first_tweet = dtemp.local_time.min()
            print(first_tweet)
            dtemp1 = dtemp.loc[(dtemp["local_time"] >= first_tweet) &
                               (dtemp["local_time"]< first_tweet+timedelta(minutes = int(minute_interval)))]
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

    dict_data = {"user_screen_name": list_user, "text":list_text, "min_date": list_min_date, "max_date":list_max_date}
    dg = pd.DataFrame(dict_data)
    dg["year"]= dg.min_date.dt.year
    dg["month"]= dg.min_date.dt.month
    dg["day"]= dg.min_date.dt.day
    dg["hour"]= dg.min_date.dt.time
    dg["date"] = dg.min_date.dt.date
    dg["source"] = "Twitter"
    dg = dg.merge(data[["user_screen_name","user_description"]].drop_duplicates(), on = ["user_screen_name"], how = "left")

    return dg
