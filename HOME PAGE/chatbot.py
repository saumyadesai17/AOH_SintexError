import google.generativeai as palm
from dotenv import load_dotenv
import os

load_dotenv()

palm_api_key = os.getenv('PALM_API_KEY')

palm.configure(api_key=palm_api_key)
print("Welcome to Personal Assistant Chatbot !")
print("Type 'exit' to end the chat")

while(True):
    str=input("You: ")

    if(str=="exit"):
        print("Please visit again")
        break
    
    else:
        response = palm.chat(messages=str)
        print(f"ChatBot: {response.last}")
