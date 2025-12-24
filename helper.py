from dotenv import load_dotenv
import os
import streamlit as st

def getAPIKey():
    load_dotenv()
    API_KEY = os.getenv('API_KEY')
    return API_KEY

class Message:
    def __init__(self, role, text):
        self.role = role
        self.text = text
        self.showMessage()

    def showMessage(self):
        message = st.chat_message(self.role)
        message.write(self.text)


