import streamlit as st

from google.cloud import firestore

from google.oauth2 import service_account
import json


# @st.cache_resource
# def init_connection():
#     # return firestore.Client()
#     return

key_dict = json.loads(st.secrets["FIRESTORE_KEY"])

creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)
# db = firestore.Client.from_service_account_json("firebase-key.json")

doc_ref = db.collection("books")

try:
    docs = doc_ref.stream()
    for doc in docs:
        st.write(f"{doc.id} => {doc.to_dict()}")
except:
    st.write("No such document!")

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

# Use the json key generated from the Firebase console
# if not firebase_admin._apps:
#     cred = credentials.Certificate("firebase-key.json")
#     firebase_admin.initialize_app(cred)

# db = firestore.client()
# with open("firebase-key.json") as json_file:
#     json_text = json_file.read()
#     print(json_text)

# key_dict = json.loads(st.secrets["FIRESTORE_KEY"])

# creds = service_account.Credentials.from_service_account_info(key_dict)
# db = firestore.Client(credentials=creds)


# def getDocuments():
#     st.write("## Get documents")
#     # db = firestore.Client.from_service_account_json("firebase-key.json")
#     # print(db)
#     doc_ref = db.collection("books").document("documento")
#     try:
#         doc = doc_ref.get()
#         st.write(doc.to_dict())
#     except:
#         st.write("No such document!")

# # doc = doc_ref[0]
# # if doc.exists:
# #     st.write(f"Document data: {doc.to_dict()}")
# # else:
# #     st.write("No such document!")


def app():
    st.title("Pixelspace Experiments")
    st.write("This is the home page of the experiments project.")


st.title("Pixelspace Experiments")

st.write("This is the home page of the experiments project.")

# getDocuments()
