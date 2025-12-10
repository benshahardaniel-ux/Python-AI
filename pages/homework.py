from helper import *
import streamlit as st

from helper import getAPIKey

st.set_page_config(
    page_title="Daniel's Projects",
    page_icon="👑",
    layout="wide"
)

st.title("Homework bot")

API_KEY = getAPIKey()