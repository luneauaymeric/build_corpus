# Build corpus: corpus construction for Prospéro

Streamlite application developed as part of the Amulex project to build Prospéro corpora from .csv files or a postgresql database.

Application inspired by :

- “Outil pour les Enquêtes Numériques” by Émilien Schultz: [https://github.com/emilienschultz/dstool](https://github.com/emilienschultz/dstool)

- Tiresias: [https://github.com/josquindebaz/Tiresias](https://github.com/josquindebaz/Tiresias)

## Local installation with Docker

### Linux

- Go to the folder where you want to put the local repository
- Run ``git clone [app_URL]`` (you must have git installed)
- Make a copy of the streamlit.sample folder and rename it .streamlit
- Within this folder, configure the file secrets.toml
- If you want to change the default application port (8501), copy the env.sample file, rename it to .env and change the parameter
- run ``docker compose up --build`` (you must have docker installed)
- Go to the address indicated on the terminal (default: http://localhost:8501)

## How it works

This application does two things:


1. Read texts while preserving “html” enrichments (emoji, links, etc.)

2. Create a corpus that can be read on Prospéro


### Loading data from a csv file

First of all, you can display data from a csv file if you have one. This CSV file must contain at least the following three columns:

- An “Author” column

- A “Text” column

- A “Date” column (in YYYY-MM-DD format)


|Author | Text | Date |
|-------|------|------|
| X | lllll| YYYY-MM-DD|


Once the file is loaded, various widgets in the sidebar allow you to change the “Author” column (if you want to use the user_name instead of the user_screen_name, for example), specify the source of the texts (Twitter, Twitch, etc.), filter the texts according to a certain word threshold.

### Loading data from the database

Data can also be loaded directly from the Amulex postgresql database. For the moment, we have access to publications from three platforms: Twitch, Twitter and Youtube.

Two widgets allow you to filter the data according to one or more shows and one or more candidates.

Of course, you can choose to display all the publications linked to one platform at a time. However, the sheer volume of data makes the display very slow. It is therefore advisable to use one of the two filters.

#### How filters work:
Filters work differently for different platforms.

For __Twitch__, the search is based on the list of issues collected -- [the list can be found here](https://raw.githubusercontent.com/luneauaymeric/build_corpus/main/script/liste_emission.csv) -- and entered in Zotero. Only those broadcasts that correspond to the chosen criteria are retained. For example, if I choose the program _Backseat_, the script performs an initial filter, retaining only those programs whose “publication_title” column contains “Backseat”. The same applies to candidates. We can then combine these two criteria, keeping only _Backseat_ programs in which Jadot was a guest, for example.

We then use the “publication_id” of the shows corresponding to the filter criteria to send a query to the database and retrieve all comments posted at the time of the show. This query takes the following form:

```
SELECT ta.firstname, t.text_content, t.text_content_creation_date, t.id, t.publication_id, t.person_id FROM public.twitch_comment t JOIN public.person ta ON t.person_id = ta.id WHERE t.publication_id in (list_publi_id)'
```

For __Twitter__, the search is based on show and candidate hashtags. Note that the combination of the two criteria corresponds to a non-exclusive 'OR'. In other words, the query will return all tweets containing the hashtag #Basckseat or the hashtag #Jadot, for example. In the list of publications, we'll therefore also have tweets about Backseat shows with Zemmour (if any) or shows with Jadot other than Backseat. This query takes the following form:

```
SELECT publication_id, text_content, person_id, pub_date FROM public.twitter_post WHERE text_content NOT LIKE \'RT%\' AND text_content SIMILAR TO '%(#Jadot|#Backseat)%''
```

Note that retweets are excluded ('NOT LIKE RT').


### Creating a corpus
Finally, the corpus construction tool appears:

- Remember to enter the address where the files will be located (the folder in which the txt and prc files will be stored). Without this address, the (create corpus) button will not work. It is used to write the “.prc” file, the one used in Prospéro to load a corpus.

Once the address has been entered and the “Create corpus” button pressed, the text files are temporarily saved in a zip file, which can then be downloaded using the button provided.

[https://raw.githubusercontent.com/luneauaymeric/build_corpus/main/streamlit-lecteur_tweets-2024-05-30-18-05-92.webm](https://raw.githubusercontent.com/luneauaymeric/build_corpus/main/streamlit-lecteur_tweets-2024-05-30-18-05-92.webm)



