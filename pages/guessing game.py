import os #operating system מערכת הפעלה
from dotenv import load_dotenv #הספרייה שהורדנו של משתני הסביבה
from google import genai #בינה מלאכותית יוצרת
import streamlit as st #ספרייה של ממשקים GUI
from streamlit import session_state
from helper import *

st.set_page_config(
    page_title="Guessing Game",
    page_icon="Bot"
)

newPage("Guessing Game")

st.title("AI guessing game")

load_dotenv() #טוענים את המשתנים
API_KEY = os.getenv("API_KEY") #פונים לקובץ env - ומבקשים את המשתנה API_KEY

def start():
    st.session_state.game_over = False
    st.session_state.gemini = genai.Client(api_key=API_KEY)
    st.session_state.history = []
    message = send(prompt)
    #st.text(message)
    #תיבת טקסט של צאט
    # ai_text = st.chat_message("ai")
    # ai_text.write(message)


gemini = genai.Client(api_key=API_KEY)

#all_models = ["gemini-2.5-flash","gemini-2.0-flash","gemini-2.5-flash-lite","gemini-2.0-flash-lite"]

def send(prompt):
    st.session_state.history.append({
        "sender" : "user",
        "text" : prompt
    })
    context = "Entire chat \n"
    for line in st.session_state.history:
        context += f"{line['sender']}: {line['text']}\n"

    with st.spinner("Thinking..."):
        for model in all_models:
            print(model)
            chat = st.session_state.gemini.chats.create(model=model) #לוקחים מסשן את מה ששמור שם
            try:
                message = chat.send_message(context)
                st.session_state.history.append({
                    "sender" : "user",
                    "text" : message.text
                })
                return message.text
            except Exception as e:
                print(e)
                print("Something went wrong, trying next model")

prompt = """
###context:
we are in a guessing game
you need to generate a random word and the player has to guess it
you need to give the hints

###rules:
the word or a different version of the word cant appear as a hint
dont let the player see the word
make the first hint more general and after make it more specific

###end of game
after 3 tries or success
**reveal the word
**you type "WIN" if the player guessed correctly
**you type "LOSE" if the player guessed incorrectly on the last attempt
**you type each response on its own line
**you type "END" on a new line after WIN or LOSE to end the game
"""

print("starting...")
#chat = gemini.chats.create(model="gemini-2.5-flash")
print("connecting to gemini...")

if "gemini" not in session_state: #אם אין לך גמיני
    start() #תפעיל את הפונקציה של ההתחלה

if "history" in st.session_state and len(session_state["history"]) > 0:
    for line in st.session_state.history[1:]:
        chat = st.chat_message(line["sender"])
        chat.write(line["text"])

# message = send(prompt)
# st.text(message)

# if "game_over" not in st.session_state:
#     st.session_state.game_over = False
# if "ai" not in st.session_state:
#     st.session_state.ai = ""

if "game_over" in st.session_state and st.session_state.game_over:
    st.balloons()
    st.success("game over")

else:
    user = st.chat_input("guess", key="guess_input", disabled=st.session_state.game_over)
    if user:
        user_text = st.chat_message("user")
        user_text.write(user)

        ai = send("my guess: " + user)
        ai_text = st.chat_message("ai")
        ai_text.write(ai)

        if "END" in ai:
            st.session_state.game_over = True
            st.rerun()

#print(message)

# while True:
#     print(message.text)
#
#     prompt = input("\n")
#
#     if "END" in message.text:
#         break


# to = input("who is the letter for?")
# content = input("what is the letter about?")
# addons = input("something important you want to add?")
# #הנחייה לAI
# prompt = (f"you are very good at writing letters"
#           f"write a letter to {to}"
#           f"the letter is about {content}"
#           f"also pay attention to this: {addons}")
#
#
# #print(API_KEY) בדיקה שמצא
# gemini = genai.Client(api_key=API_KEY) #צד קליינט
# ai = gemini.chats.create(model="gemini-2.0-flash") #מודל גמיני
# message = ai.send_message(prompt)
# print(message.text)

