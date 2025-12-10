from dotenv import load_dotenv
import os

def getAPIKey():
    load_dotenv()
    API_KEY = os.getenv('API_KEY')
    return API_KEY