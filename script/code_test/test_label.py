from random import randrange
from typing import List

import lorem
import streamlit as st

from streamlit_text_label import Selection, label_select

import visualisation

@st.cache_data
def get_body():
    text_body= "Avec votre accord, nous et nos 297 partenaires utilisons des cookies ou technologies similaires pour stocker, consulter et traiter des données personnelles telles que votre visite sur ce site internet, les adresses IP et les identifiants de cookie. Certains partenaires ne demandent pas votre consentement pour traiter vos données et se fondent sur leur intérêt commercial légitime. À tout moment, vous pouvez retirer votre consentement ou vous opposer au traitement des données fondé sur l'intérêt légitime en cliquant sur « En savoir plus » ou en allant dans notre politique de confidentialité sur ce site internet."
    #text_body = visualisation.display_text(data=df)
    return text_body


@st.cache_data
def get_labels():
    return ["Entité", "Epreuve", "Qualité","Marqueur", "Catégorie", "Etre ficitif"]

@st.cache_resource
def get_selections(count: int = 5) -> List[Selection]:
    #body = get_body()
    labels = get_labels()
    selected = []
    # for n in range(count):
    #     i = randrange(len(body))
    #     start = i
    #     while start > 0 and not body[start].isspace():
    #         start -= 1
    #     end = i
    #     while end < len(body) and not body[end].isspace():
    #         end += 1
    #     text = body[start:end]
    #     label = labels[n % len(labels)]
    #     selected.append(Selection(start=start, end=end, text=text, labels=[label]))
    return selected





def main():
    st.title("Component Gallery")
    st.header("Label selected text")
    st.markdown(
        """
        To add a new annotation

        1. Pick a label
        2. Highlight text with cursor

        To delete an annotation

        1. Click highlighted text
        2. Press backspace

        Finally, click `Update` to propagate changes to streamlit.
        """
    )
    selected = label_select(
        body=get_body(),
        labels=get_labels(),
        selections=get_selections(),
    )
    st.write(selected)

def side():
    st.sidebar.title("Chargement d'un fichier CSV")
    uploaded_files = st.sidebar.file_uploader("Téléverser le fichier csv", accept_multiple_files=False)


if __name__ == "__main__":
    main()
    side()
