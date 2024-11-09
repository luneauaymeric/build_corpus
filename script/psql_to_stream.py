import streamlit as st
import grouping_post as gp
import pandas as pd


@st.cache_data
def connect_twitch(_conn, list_publi_id):
    print("len list_pub_id : ", list_publi_id)
    if len(list_publi_id) > 1 :
        df = _conn.query(f'SELECT ta.firstname, t.text_content, t.text_content_creation_date, t.id, t.pub_reference_id, t.person_id FROM public.twitch_comment t  JOIN public.person ta ON t.person_id = ta.id WHERE t.pub_reference_id in {tuple(list_publi_id)}', ttl="10m")
    else  :
        df = _conn.query(f'SELECT ta.firstname, t.text_content, t.text_content_creation_date, t.id, t.pub_reference_id, t.person_id FROM public.twitch_comment t  JOIN public.person ta ON t.person_id = ta.id WHERE t.pub_reference_id = \'{list_publi_id[0]}\'', ttl="10m")
    df2 = _conn.query('SELECT person_id, description FROM public.twitch_account', ttl="10m")
    print(len(df))
    dict_desc = dict(zip(df2.person_id, df2.description))
    new_column_name = {"pub_reference_id":"twitch_id", "text_content":"text", "firstname": "author",  "text_content_creation_date":"local_time"}
    df= df.rename(columns = new_column_name)
    df["description"] = df.person_id.map(dict_desc)
    #df = df.merge(dfe[""])
    return df

@st.cache_data
def connect_twitter(_conn, liste_hashtag):
    if len(liste_hashtag) > 1 :
        pattern_hash = '|'.join(liste_hashtag)
        df = _conn.query(f'SELECT publication_id, text_content, person_id, pub_date FROM public.twitter_post WHERE text_content NOT LIKE \'RT%\' AND text_content SIMILAR TO \'%({pattern_hash})%\'', ttl="10m")
    elif len(liste_hashtag) == 1 :
        pattern_hash = f'%{liste_hashtag[0]}%'
        df = _conn.query(f'SELECT publication_id, text_content, person_id, pub_date FROM public.twitter_post WHERE text_content NOT LIKE \'RT%\' AND text_content LIKE \'{pattern_hash}\'', ttl="10m")
    elif len(liste_hashtag) == 0 :
        df = _conn.query(f'SELECT publication_id, text_content, person_id, pub_date FROM public.twitter_post WHERE text_content NOT LIKE \'RT%\'', ttl="10m")
    df2 = _conn.query('SELECT person_id, screen_name, description FROM public.twitter_account', ttl="10m")
    dict_name = dict(zip(df2.person_id, df2.screen_name))
    dict_desc = dict(zip(df2.person_id, df2.description))
    df["author"] = df.person_id.map(dict_name)
    df["description"] = df.person_id.map(dict_desc)


    #df3 = _conn.query('''SELECT t.publication_id, ta.pub_date FROM public.twitter_post t JOIN public.publications ta ON t.publication_id=ta.id''', ttl="10m")
    #print('taille df3 ', len(df3))
    #dict_date = dict(zip(df3.publication_id, df3.pub_date))
    #df["local_time"] = df.publication_id.map(dict_date.get)
    new_column_name = {"publication_id":"id", "text_content":"text", "person_id":"user_id", "pub_date":"local_time"}
    df =df[["author", "text_content", "pub_date", "publication_id", "person_id", "description"]].rename(columns = new_column_name)
    print('taille df ', len(df))
    return df
    #st.dataframe(data=df)

@st.cache_data
def connect_youtube(_conn, list_publi_id):
    print("len list_pub_id : ", tuple(list_publi_id))
    if len(list_publi_id) > 1 :
        df = _conn.query(f'SELECT ta.name, t.person_id, t.text_content, t.date, t.id, t."isReplyTo", t.comment_id, t.publication_id   FROM public.youtube_comment t JOIN public.youtube_account ta ON t.person_id = ta.person_id WHERE t.publication_id in {tuple(list_publi_id)}', ttl="10m")
    else :
        df = _conn.query(f'SELECT ta.name, t.person_id, t.text_content, t.date, t.id, t."isReplyTo", t.comment_id, t.publication_id   FROM public.youtube_comment t JOIN public.youtube_account ta ON t.person_id = ta.person_id WHERE t.publication_id = \'{list_publi_id[0]}\'', ttl="10m")
    dict_comment_id = dict(zip(df.comment_id, df.id))
    dict_comment_person = dict(zip(df.comment_id, df.person_id))
    dict_comment_person_name = dict(zip(df.comment_id, df.name))
    df["id_reply"] = df.isReplyTo.map(dict_comment_id.get)
    df["person_id_reply"] = df.isReplyTo.map(dict_comment_person.get)
    df["person_name_reply"] = df.isReplyTo.map(dict_comment_person_name.get)

    new_column_name = {"name":"author", "text_content":"text", "date":"local_time"}
    df= df.rename(columns = new_column_name)

    
    return df



# Print results.
#st.dataframe(data=df)postgresql://username:password@postgres:5432/dbname
