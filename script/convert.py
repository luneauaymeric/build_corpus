""" From FACTIVA hml to Prospéro Files  TXT and CTX
Josquin Debaz
GNU General Public License
Version 3, 29 June 2007
"""

import re
import os
import glob
import random
import datetime
import csv
import pandas as pd
import zipfile
import io
import cleaning
from cleaning import Cleaner
import emoji
# try:
#     import cleaning
# except:
#     from mod.cleaning import Cleaner


def get(text, begin, end):
    """return the content between two given strings"""
    result = re.split(begin, text, 1)[1]
    result = re.split(end, result, 1)[0]
    return result


def format_date(date):
    """return the number of a French or English month"""
    months = {
        "janvier": "01",
        'février': "02",
        "mars": "03",
        "avril": "04",
        "mai": "05",
        "juin": "06",
        "juillet": "07",
        "août": "08",
        "septembre": "09",
        "octobre": "10",
        "novembre": "11",
        "décembre": "12",
        "January": "01",
        'February': "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12"
    }
    try:
        date = re.split(" ", date)
        day = "%02d" % int(date[0])  # day with 2 digits
        return "%s/%s/%s" % (day, months[date[1]], date[2][:4])
    except:
        return "00/00/0000"


def file_name(date, prefix, save_dir, list_path_file):
    """return a name in Prospero style"""
    index, base = "A", 64
    date = "".join(reversed(date.split("/")))
    name = "%s%s%s" % (prefix, date, index)
    path = os.path.join(save_dir, name + ".txt")
    while name in list_path_file:
        if ord(index[-1]) < 90:
            index = chr(ord(index[-1]) + 1)
        else:
            base += 1
            index = "A"
        if base > 64:  # if Z => 2 letters
            index = chr(base) + index
        name = "%s%s%s" % (prefix, date, index)
        path = os.path.join(save_dir, name + ".txt")
    return name



class ParseCsv:
    """from htm of csv to Prospero"""

    def __init__(self, fname):
        self.content = pd.read_csv(fname, sep=";", encoding="utf-8")

    # def get_supports(self, fname):
    #     """parse supports.publi and find correspondences"""
    #     medias = {}
    #     with open(fname, 'rb') as file:
    #         buf = file.read()
    #         try:
    #             buf = buf.decode('utf8') #byte to str
    #         except:
    #             buf = buf.decode('latin-1')
    #         lines = re.split("\r*\n", buf)
    #     for line in lines:
    #         media = re.split('; ', line)
    #         if media:
    #             medias[media[0]] = media[1:]

    #     for key, article in self.articles.items():
    #         if article['media'] in medias.keys():
    #             self.articles[key]['support'] = medias[article['media']][0]
    #             self.articles[key]['source_type'] = medias[article['media']][1]
    #             self.articles[key]['root'] = medias[article['media']][2]
    #         else:
    #             if article['media'] not in self.unknowns:
    #                 self.unknowns.append(article['media'])
    #             self.articles[key]['support'] = article['media']
    #             self.articles[key]['source_type'] = 'unknown source'
    #             self.articles[key]['root'] = 'FACTIVA'
    #@st.cache_data
    def write_prospero_files(self, save_dir, observation, cleaning=False):

        """for each article, write txt, csv and ctx in a given directory"""
        dict_mois = {"10":"A", "11":"B", "12":"C"}
        zip_buffer = io.BytesIO()
        print("save_dir : ", save_dir)
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            dictio_elem = "/home/aymeric/corpus/0_dic/dic_elementaires/"
            dictio_fic = "/home/aymeric/corpus/0_dic/Etre_fictif/EF_pesti_medialab.fic"
            dictio_cat = "/home/aymeric/corpus/0_dic/Categories/Cat_pesti_medialab.CAT"
            dictio_col = "/home/aymeric/corpus/0_DIC/COLLECTIONS/Coll_pesti_medialab.col"
            prc_txt= ["projet0005", dictio_elem, dictio_fic, dictio_cat, dictio_col, "français"]

            list_path_file =[]

            for _, row in self.iterrows():
                jour = str(row["day"])
                if len(jour) == 1:
                    jour_prospero = "0"+jour
                else:
                    jour_prospero = jour
                mois = str(row["month"])
                if len(mois) == 1:
                    mois_prospero = str(mois)
                    mois= f"0{mois}"
                else:
                    mois_prospero= dict_mois[str(mois)]
                annee = str(row["year"])
                date_prospero = "%s/%s/%s" % (jour_prospero, mois_prospero, annee[2:])
                date_ctx = "%s/%s/%s" % (jour_prospero, mois, annee)
                heure_pub = str(row["hour"])
                rac = str(row["source"])
                if rac == "Twitch":
                    rac = "TWIC"
                elif rac == "Twitter":
                    rac = "TWIT"
                else:
                    rac = rac[0:4].upper()

                date = "".join(reversed(date_prospero.split("/")))
                filepath = "%s%s%s%s" % (rac, date, "_", _)

                #filepath = file_name(date_prospero, rac, save_dir, list_path_file)
                #path = os.path.join(filepath + ".txt")
                path = filepath+".txt"

                list_path_file.append(filepath)

                full_filepath = f"{save_dir}/{path}".replace('//', '/')
                

                prc_txt.append(full_filepath)

                auteur = str(row["author"])
                title = f"Posts de {auteur}"
                #titulo = title + "\r\n"
                #ponto = ".\r\n"
                texto = str(row["text"])
                part_of_text = "\r\n.\r\n".join([title, texto])
                part_of_text = emoji.demojize(part_of_text, language='fr')
                C = Cleaner(part_of_text.encode("utf-8"), options="uasdhtpcef")
                C_latin = bytes(C.content, 'latin-1')
                zip_file.writestr(path, C_latin)


            #ed = f'\ ED: {row["ED"]}'
            #pg_se = f'PG: {row["PG"]} / SE: {row["SE"]} '.replace("\\", " ")
                ctx = ["fileCtx0005",
                        title,
                        str(row["author"]),
                        "",
                        "",
                        date_ctx,
                        str(row["source"]),
                        "Réseau social",
                        observation,
                        "",# nom de l'emission de référence
                        "",
                        "Processed by Tiresias on %s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "",
                        "n",
                        "n",
                        f"REF_HEURE:{heure_pub}" # heure de publication
                        ] #hour ?]

                ctx = "\r\n".join(ctx)
                ctx = emoji.demojize(ctx, language='fr')
                Ctx = Cleaner(ctx.encode("utf-8"), options="ua")
                Ctx_latin = bytes(Ctx.content, 'latin-1')
                path = os.path.join(filepath + ".ctx")
                zip_file.writestr(path, Ctx_latin)

            prc_txt.append("ENDFILE")
            prc_file = "\r\n".join(prc_txt)

            nom_support= "corpus"
            path_prc = nom_support.lower().replace(" ","_")+".prc"
            zip_file.writestr(path_prc, prc_file.encode('latin-1'))
        buf = zip_buffer.getvalue()
        zip_buffer.close()
        return buf





if __name__ == "__main__":
    SUPPORTS_FILE = "support.publi"
    for filename in glob.glob("*.csv"):
        print(filename)
        run = ParseCsv(filename)
        # print("%s: found %d article(s)"%(filename, len(run.content)))
        # run.get_supports(SUPPORTS_FILE)
        # print("%d unknown(s) source(s)" %len(run.unknowns))
        # for unknown in run.unknowns:
        #     print("unknown: %s" % unknown)
        # run.write_prospero_files(".")
