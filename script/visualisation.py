import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

@st.cache_data
def display_text(data):
    for n, x in enumerate(data.text):
        if 'user_screen_name' in data.columns:
            st.write('__Name:__ ', data['user_screen_name'].iloc[n])
        elif 'author' in data.columns:
            st.write('__Name:__ ', data['author'].iloc[n])

        if "User_status" in data.columns:
            st.write('__Statut:__ ', data['User_status'].iloc[n])
        else:
            pass
        #st.write(x)
        if "reply_to" in data.columns:
            if data.retweeted_id.isnull().iloc[n] == False:
                st.write('__retweet de :__ ', data['retweeted_user_id'].iloc[n])
            else:
                pass
        else:
            pass
        if "local_time" in data.columns:
            st.write('__Date:__ ', data['local_time'].iloc[n])
        else:
            pass

        st.write('__Emission:__', data['Publication Title'].iloc[n])
        st.write('__Candidat.e:__', data['Guest'].iloc[n])
        #st.write('Organ: ', tweets['Organ'].iloc[n])
        st.write(x)
        st.divider()

# Fonction pour tracer la série temporelle
# Fonction pour tracer la série temporelle
@st.cache_data
def tracer_graphique(data, d):
    scale = {"Année":"y","Mois":"m","Jour":"d"}
    df1 = data.groupby(["local_time"]).agg(nb=('id','size')).reset_index()
    #df["num"] = 1 # valeur par article pour comptage
    leg = []
    fig,ax=plt.subplots(1,figsize=(10,3))
    if "User_status" in data.columns:
        for i, j in data.groupby("User_status"):
            leg.append(i)
            j.set_index("date")["id"].resample(scale[d]).size().plot(ax=ax,style=".-")
        plt.legend(leg)
    else:
        #data.set_index("date")["id"].resample(scale[d]).size().plot(ax=ax,style=".-")
        plt.plot(df1.local_time, df1.nb)
    plt.title("Evolution temporelle du dataframe original")
    plt.xlabel("Temps (par %s)"%d)
    plt.ylabel("Nombre de tweets")
    plt.tight_layout()
    return fig

@st.cache_data
def display_dataframe(data):
    try:
        data = data[["author", "text", "local_time", "source","Publication Title","Guest"]].sort_values("local_time",ascending=True).reset_index().drop(columns=["index"])
    except:
         data = data[["author", "text", "local_time", "source"]].sort_values("local_time",ascending=True).reset_index().drop(columns=["index"])
    st.dataframe(data)


def display_quote1(data):
    index = st.session_state.count
    print(index)
    if 'user_screen_name' in data.columns:
        st.write('__Name:__ ', data['user_screen_name'].iloc[index])
    elif 'author' in data.columns:
        st.write('__Name:__ ', data['author'].iloc[index])

    if "User_status" in data.columns:
        st.write('__Statut:__ ', data['User_status'].iloc[index])
    else:
        pass
    #st.write(x)
    if "reply_to" in data.columns:
        if data.retweeted_id.isnull().iloc[n] == False:
            st.write('__retweet de :__ ', data['retweeted_user_id'].iloc[index])
        else:
            pass
    else:
        pass
    if "local_time" in data.columns:
        st.write('__Date:__ ', data['local_time'].iloc[index])
    else:
        pass
    #st.write('Organ: ', tweets['Organ'].iloc[n])
    st.write(data.text.iloc[index])
    st.divider()
