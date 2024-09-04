# Build corpus : construction de corpus pour Prospéro

Application streamlite développé dans le cadre du projet Amulex pour construire des corpus Prospéro à partir de fichiers .csv ou d'une base de donnée postgresql

Application inspirée de :

- "Outil pour les Enquêtes Numériques" d'Émilien Schultz : [https://github.com/emilienschultz/dstool](https://github.com/emilienschultz/dstool)

- Tiresias : [https://github.com/josquindebaz/Tiresias](https://github.com/josquindebaz/Tiresias)

## Installation locale avec Docker

### Linux

- Mettez vous sur le dossier où vous voulez mettre le dépôt local
- Faites ```git clone [app_URL]``` (il faut avoir git installé)
- Faites une copie du dossier streamlit.sample et rennomez-le en .streamlit
- À l'intérieur de ce dossier, configurez le fichier secrets.toml
- Si vous voulez changer la porte de l'application par défaut (8501), copiez le fichier env.sample, renommez-le en .env et changez le paramètre
- faites ```docker compose up --build``` (il faut avoir docker installé)
- Allez sur l'adresse indiqué sur le terminal (par défaut: http://localhost:8501)

## Fonctionnement

Cette application permet de faire deux choses :


1. Lire les textes en conservant les enrichissement "html" (emoji, lien, etc.)

2. Créer un corpus qui pourra être lu sur Prospéro


### Chargement des données à partir d'un csv

Il est tout d'abord possible d'afficher les données d'un fichier csv si on en dispose un. Ce fichier CSV doit contenir au moins les trois colonnes suivantes:

- Une colonne "Author"

- Une colonne "Text"

- Une colonne "Date" (au format YYYY-MM-DD)


|Author | Text | Date |
|-------|------|------|
| X     | lllll| YYYY-MM-DD|


Une fois le fichier chargé, dans la barre latéral, différents widget permettent de changer la colonne "Author" (si on veut utiliser le user_name à la place du user_screen_name par exemple), de préciser la source des textes (Twitter, Twitch, etc.), de filtrer les textes en fonction d'un certain seuil de mots.

### Chargement des données depuis la base de donnée

On peut aussi charger les données directement depuis la base de donnée postgresql d'Amulex. Pour le moment, on a accès aux publication de trois plateformes : Twitch, Twitter, Youtube.

Deux widget permettent de filtrer les données en fonction d'une ou plusieurs émissions et d'un.e ou plusieurs candidat.es.

Bien sûr, on peut décider d'afficher toutes les publications liées à une plateforme à la fois. Toutefois, la masse de données rend l'affichage très lent. Il est donc conseillé d'utiliser un des deux filtres.

#### Fonctionnement des filtres:
Les filtres fonctionnent différemment en fonction des plateforme.

Pour __Twitch__, la recherche se base sur la liste des émissions collectées -- [la liste se trouve ici](https://raw.githubusercontent.com/luneauaymeric/build_corpus/main/script/liste_emission.csv) -- et renseignées dans Zotero. On conserve alors uniquement les émissions qui correspondent aux critères choisis. Ainsi si je choisi l'émission _Backseat_, le script opère un premier filtre en conservant uniquement les émissions dont la colonne "publication_title" contient "Backseat". Idem pour les candidat.es. On peut ensuite combiner ces deux critères : conservé uniquement les émissions _Backseat_ dans lesquelles Jadot a été invité par exemple.

On utilise ensuite les "publication_id" des émissions correspondant aux critères de filtre pour envoyer une requête à la bases de donnée et récupérer tous les commentaires postées au moment de l'émission. Cette requête prend la forme suivante :

```
SELECT ta.firstname, t.text_content, t.text_content_creation_date, t.id, t.publication_id, t.person_id FROM public.twitch_comment t  JOIN public.person ta ON t.person_id = ta.id WHERE t.publication_id in (list_publi_id)'
```

Pour __Twitter__, la recherche se base sur les hashtags des émissions et des candidats. Attention ici la combinaison des deux critères correspond à un 'OU' non exclusif. C'est-à-dire que la requête retournera tous les tweets qui contiennent le hashtag #Basckseat ou le hashtag #Jadot par exemple. Dans la liste des publications, on aura donc aussi des tweets sur les émissions Backseat avec Zemmour (s'il y en aune) ou les émissions avec Jadot autres que Backseat. Cette requête prend la forme suivante:

```
'SELECT publication_id, text_content, person_id, pub_date FROM public.twitter_post WHERE text_content NOT LIKE \'RT%\' AND text_content SIMILAR TO '%(#Jadot|#Backseat)%'
```

On remarque que les retweets sont exclus ('NOT LIKE RT').



### Création d'un corpus
Enfin, on voit apparaître l'outil de construction du corpus :

- Il faut bien penser à renseigner l'adresse de localisation des fichiers (le dossier dans lequel seront conservés les fichiers txt et prc). Sans cette adresse le bouton (créer le corpus ne fonctionnera pas). Elle est utilisée pour écrire le fichier ".prc", celui qu'on utilise dans Prospéro pour charger un corpus.

Une fois l'adresse renseignée et le bouton "Créer un corpus" actionné, les fichiers textes sont enregistrés temporairement dans un fichier zip que l'on peut ensuite télécharger grâce au bouton prévu à cette effet.

[https://raw.githubusercontent.com/luneauaymeric/build_corpus/main/streamlit-lecteur_tweets-2024-05-30-18-05-92.webm](https://raw.githubusercontent.com/luneauaymeric/build_corpus/main/streamlit-lecteur_tweets-2024-05-30-18-05-92.webm)
