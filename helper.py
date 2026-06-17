from dotenv import load_dotenv
import os
import streamlit as st
from google import genai
from google.genai import types
import time
from ddgs import DDGS

def web_search(query : str) -> str:
    print("searching: " + query)
    """
    
    function that gets terms to search and returns top search results 
    function gets text to search and returns results 
    """
    with st.status("searching" + query):
        with DDGS() as d:
            results = d.text(query,max_results=3)
            return results

st.session_state.page = ""
def newPage(pagename):
    if "page" not in st.session_state:
        st.session_state.page = ""
    if st.session_state.page != pagename:
        print("new page")
        st.session_state.page = pagename
        st.session_state.history = []

all_models = [
    "gemini-3.1-flash-lite", #500 הודעות ביום
    "gemini-2.5-flash-lite", #20 הודעות
    "gemini-2.5-flash", #10 הודעות
   # "gemini-2.0-flash",
    "gemini-3-flash",
    "gemini-3-flash-preview"
   # "gemini-2.0-flash-lite"
]
def currentTime():
    print("use tool")
    """
    tool that knows what the time is now and returns text of the current time 
    """
    return time.ctime()


def create_chat(model,instruction,history=[]):  #מקבל מודל והיסטוריה - לרוב ריקה
    if "client" not in st.session_state: #אם אין קליינט בזיכרון
        st.session_state.client = genai.Client(api_key=getAPIKey()) #יוצר קליינט עם הAPI Key
    if instruction == "": #אם אין הוראות
        if "system_prompt" in st.session_state: #תבדוק האם הגדרנו פרומפט
            instruction = st.session_state.system_prompt
    #print(instruction)
    st.session_state.chat  = st.session_state.client.chats.create(
        model = model,
        history= history,
        config = types.GenerateContentConfig(
            system_instruction = instruction,   #ההוראות לג'מיני
            tools = [currentTime, web_search], #מה הוא יכול לעשות
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False) #תפעיל את הטול אם אתה רוצה
        )
    ) #יוצרים צ'אט במודל ששלחנו


st.session_state.modelIndex = 0 #מתחילים מהמודל הראשון
maxTries = 5
currentTries = 0

if "history" not in st.session_state:
    st.session_state.history = []

def sendMessage(prompt, image=None): #פונקציה ששולחת הודעה
    st.session_state.history.append(
        {
            "role" : "user",
            "text" : prompt
        }
    )
    if "chat" not in st.session_state:
        create_chat(all_models[0], "")
    global currentTries
    print(all_models[st.session_state.modelIndex])
    context = [prompt]
    if image:
        context.append(image)
    try: #תנסה
        answer = st.session_state.chat.send_message(context)
        st.session_state.history.append(
            {
                "role" : "model",
                "text" : answer.text
            }
        )
        Message("ai", answer.text)
        currentTries = 0
        st.rerun
        #אם הוא הצליח - נמשיך מפה
    except Exception as e: #אם לא הצליח
        error = str(e) #תהפוך לטקסט
        print(e)
        currentTries += 1
        if currentTries == maxTries:
            st.error("no models are working")
            return
        if "overloaded" in error.lower(): #תבדוק האם מופיע שהסיבה היא שהמודל עמוס
            newchat(prompt, image)
        if "429" in error:
            with st.spinner("Too many requests, waiting for a minute...", show_time=True):
                time.sleep(60)
                newchat(prompt, image)
        if "503" in error:
            newchat(prompt, image)

def newchat(prompt, image=None):
    st.session_state.modelIndex += 1
    if st.session_state.modelIndex == len(all_models):
        st.session_state.modelIndex = 0
    newmodel = all_models[st.session_state.modelIndex]
    st.info(f"trying {newmodel}")
    create_chat(newmodel,"")
    sendMessage(prompt, image)

def getAPIKey():
    load_dotenv()
    API_KEY = os.getenv('API_KEY') or st.secrets['API_KEY']
    return API_KEY

class Message:
    def __init__(self, role, text):
        if role.lower == "model":
            role = "ai"
        self.role = role
        self.text = text
        self.showMessage()

    def showMessage(self):
        message = st.chat_message(self.role)
        message.write(self.text)


