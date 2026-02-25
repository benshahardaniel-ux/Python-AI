import PIL

from helper import *
import streamlit as st

from helper import *

st.set_page_config(
    page_title="Daniel's Projects",
    page_icon="👑",
    layout="wide"
)

newPage("Homework bot")

st.title("Homework bot")

API_KEY = getAPIKey()

systemPrompt = """
    # Role
    You are a homework assistant bot.

    # Task
    Your task is to help me with homework.
    Explain clearly.
    Guide me toward the correct answer.

    # Limitations
    If you don’t know — search on Google.
    **Do not make up an answer.**
    Respond like a human — in a natural way.

    **If you used a tool, write the result.**
    **We are in the year 2026.**
"""

st.session_state.systemPrompt = systemPrompt

Message("AI","How can I help you?" )

for m in st.session_state.history:
    Message(m["role"],m["text"])

userinput = st.chat_input("Enter your name")

imageinput = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if userinput:
    image = None
    if imageinput:
        image = PIL.Image.open(imageinput)
        print(image)

    Message("User", userinput)
    with st.spinner("Thinking..."):
        sendMessage(userinput, image)