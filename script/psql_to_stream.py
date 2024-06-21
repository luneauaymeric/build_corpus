import streamlit as st
import grouping_post as gp


@st.cache_data
def connect_twitch(_conn):
    df = _conn.query('''
    SELECT
    ta.firstname,
    t.text_content, t.text_content_creation_date,
    t.publication_id,
    t.person_id
    FROM public.twitch_comment t
    JOIN public.person ta
    ON t.person_id = ta.id''', ttl="10m")
    df2 = _conn.query('SELECT person_id, description FROM public.twitch_account', ttl="10m")
    dict_desc = dict(zip(df2.person_id, df2.description))
    new_column_name = {"publication_id":"id", "text_content":"text", "firstname": "author",  "text_content_creation_date":"local_time"}
    df= df.rename(columns = new_column_name).head(1000)
    df["description"] = df.person_id.map(dict_desc)

    return df

@st.cache_data
def connect_twitter(_conn, show):
    df = _conn.query(f'SELECT publication_id, text_content, person_id FROM public.twitter_post WHERE text_content NOT LIKE \'RT%\' AND "collect_filePath"=\'{show}\'', ttl="10m")
    df2 = _conn.query('SELECT person_id, screen_name, description FROM public.twitter_account', ttl="10m")
    dict_name = dict(zip(df2.person_id, df2.screen_name))
    dict_desc = dict(zip(df2.person_id, df2.description))
    df["author"] = df.person_id.map(dict_name)
    df["description"] = df.person_id.map(dict_desc)
    print('taille df ', len(df))

    df3 = _conn.query('''SELECT
    t.publication_id,
    ta.pub_date
    FROM public.twitter_post t
    JOIN public.publications ta
    ON t.publication_id=ta.id''', ttl="10m")
    print('taille df3 ', len(df3))
    dict_date = dict(zip(df3.publication_id, df3.pub_date))
    df["local_time"] = df.publication_id.map(dict_date.get)
    new_column_name = {"publication_id":"id", "text_content":"text", "person_id":"user_id"}
    df =df[["author", "text_content", "local_time", "publication_id", "person_id", "description"]].rename(columns = new_column_name)
    return df
    #st.dataframe(data=df)

# Print results.
#st.dataframe(data=df)postgresql://username:password@postgres:5432/dbname
