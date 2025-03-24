import streamlit as st
import grouping_post as gp
import pandas as pd
import emission_dictionary as ed


@st.cache_data
def connect_amulex(_conn, search_phrase, plateform):
    df = _conn.query(search_phrase, ttl="10m")

    if len(df) >0:

        dfe = ed.read_dfemission()

        if plateform == "twitch":
            df2 = _conn.query('SELECT person_id, description FROM public.twitch_account', ttl="10m")

            dict_desc = dict(zip(df2.person_id, df2.description))
            new_column_name = {"pub_reference_id":"twitch_id", "text_content":"text", "firstname": "author",  "text_content_creation_date":"local_time"}
            df= df.rename(columns = new_column_name)
            df["description"] = df.person_id.map(dict_desc)

            df0 = gp.df_processor(data=df, source = "twitch")
            df0["twitch_id"] = df0.twitch_id.astype("str")
            df0 = df0.merge(dfe[["twitch_id", "Guest", "Publication Title"]], on = ["twitch_id"], how="left")

        
        elif plateform == "youtube":
            dfe = dfe.loc[~dfe["list_youtube_id"].isna()]
            dfe["youtube_id"] = dfe["list_youtube_id"].str.split("|")
            dfexplode = dfe.explode("youtube_id")
            list_publi_id = [x for x in dfexplode.youtube_id]


            dict_comment_id = dict(zip(df.comment_id, df.id))
            dict_comment_person = dict(zip(df.comment_id, df.person_id))
            dict_comment_person_name = dict(zip(df.comment_id, df.name))
            df["id_reply"] = df.isReplyTo.map(dict_comment_id.get)
            df["person_id_reply"] = df.isReplyTo.map(dict_comment_person.get)
            df["person_name_reply"] = df.isReplyTo.map(dict_comment_person_name.get)

            new_column_name = {"name":"author", "text_content":"text", "date":"local_time"}
            df= df.rename(columns = new_column_name)

            df0 = gp.df_processor(data=df, source = "youtube")
            df0["publication_id"] = df0.publication_id.astype("str")
            df0 = df0.merge(dfexplode[["list_youtube_id", "Publication Title", "Publisher", "Guest"]].rename(columns={"list_youtube_id":"publication_id"}), on = ["publication_id"], how='left')
        
        elif plateform == "twitter":
            df2 = _conn.query('SELECT person_id, screen_name, description FROM public.twitter_account', ttl="10m")
            dict_name = dict(zip(df2.person_id, df2.screen_name))
            dict_desc = dict(zip(df2.person_id, df2.description))
            df["author"] = df.person_id.map(dict_name)
            df["description"] = df.person_id.map(dict_desc)

            df0= gp.df_processor(data=df, source = "twitter")

        st.session_state.dataframe = df0
        st.session_state.result_requests = 1
    else:
        st.session_state.result_requests = -1

