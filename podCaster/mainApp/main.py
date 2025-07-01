import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("API_KEY") #get API_KEY for the Gemini API
genai.configure(api_key=API_KEY) # type: ignore
pCaster = genai.GenerativeModel("gemini-2.5-flash")   #type:ignore
chat = pCaster.start_chat()
            

def podCaster_init(title='', topics=[]):
    response = chat.send_message(f"You are an Expert Podcast Generator, who creates extraordinary podcast content with valuable points to the listeners. Now you have to create the podcast on the title of {title} and i want to talk about the topics like {format_quests(topics)}. give me the Podcast Content for the given requirements.")
    # print("PodCaster :", response.text)
    return response.text
    
def podCaster_chat(user_msg):
    reply = chat.send_message(user_msg)
    #print("PodCaster :",response.txt)
    return reply.text
    
    

def format_quests(items):
    if not items:
        return ''
    elif len(items) == 1:
        return items[0]
    elif len(items) == 2:
        return ' and '.join(items)
    else:
        return ', '.join(items[:-1]) + ', and ' + items[-1]

