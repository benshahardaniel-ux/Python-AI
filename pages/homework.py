from helper import *
import streamlit as st

from helper import *

st.set_page_config(
    page_title="Daniel's Projects",
    page_icon="👑",
    layout="wide"
)

st.title("Homework bot")

API_KEY = getAPIKey()


Message("AI","How can I help you?" )

userinput = st.chat_input("Enter your name")

if userinput:
    Message("User", userinput)