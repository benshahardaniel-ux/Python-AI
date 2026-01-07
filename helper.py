from dotenv import load_dotenv
import os
import streamlit as st
from google import genai

all_models = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
    "gemini-3.0-flash",]

def create_chat():
    client = genai.Client(api_key=getAPIKey())


def getAPIKey():
    load_dotenv()
    API_KEY = os.getenv('API_KEY') or st.secrets['API_KEY']
    return API_KEY

class Message:
    def __init__(self, role, text):
        self.role = role
        self.text = text
        self.showMessage()

    def showMessage(self):
        message = st.chat_message(self.role)
        message.write(self.text)


