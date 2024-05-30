import streamlit as st
import io
import zipfile


def zipfile_creator():
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, data in [
            ("data1.txt", io.BytesIO(b'a,b,c')),
            ("data2.txt", io.BytesIO(b'd,e,f'))
        ]:
            zip_file.writestr(file_name, data.getvalue())
    buf = zip_buffer.getvalue()
    zip_buffer.close()
    return buf


st.header("Appname")

# create_zipfile = st.button("Create zipfile")
#
# if create_zipfile:
#     zipfile_creator()


st.download_button(
    "Download csv",
    #on_click = zipfile_creator(),
    file_name="data.zip",
    mime="application/zip",
    data=zipfile_creator()
)
