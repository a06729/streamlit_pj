import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import streamlit as st
import json


    
if not firebase_admin._apps:
    key_dict = json.loads(st.secrets["textkey"])
    # Use a service account.
    cred = credentials.Certificate(key_dict)

    app = firebase_admin.initialize_app(cred)



db = firestore.client()

def sing(id,password):
   doc_ref =db.collection("users").document(id)
   doc_ref.set({"id":id,"password":password})
def login(id,password):
    doc_ref=db.collection("users").document(id)
    doc=doc_ref.get()
    user_dict=doc.to_dict()
    print(user_dict)
    return user_dict
def saveScore(id,value):
    doc_ref=db.collection("users").document('score')
    doc_ref.set({
        "id":id,
        "score":value
    })
    
# doc_ref = db.collection("users").document("alovelace2")
# doc_ref.set({"first": "에이다", "last": "Lovelace", "born": 1815})
# doc_ref2=db.collection("users").document("alovelace2")
# doc_ref2.update({
#     "first":"에이다 웡",
#     "born":"1998"
# })