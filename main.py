import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("API_KEY") #get API_KEY for the Gemini API
genai.configure(api_key=API_KEY) # type: ignore

def getInput() -> list:
    title = input("What is the title or content you want to talk about in the Podcast ?")
    
    print("Enter some of the topics you want to talk in the podcast...\n Enter no or n to exit.")
    quests = []
    i=1
    while(True):
        print("Qn -",i)
        temp = input()
        if temp == 'n' or temp == 'no':
            break
        quests.append(temp)
        i+=1
    
    return [title,quests]
            

def podCaster():
    user_input = getInput()
    
    pCaster = genai.GenerativeModel("gemini-2.5-flash") # type: ignore
    
    chat = pCaster.start_chat()
    
    response = chat.send_message(f"You are an Expert Podcast Generator, who creates extraordinary podcast content with valuable points to the listeners. Now you have to create the podcast on the title of {user_input[0]} and i want to talk about the topics like {format_quests(user_input[1])}. give me the Podcast Content for the given requirements.")
    print("PodCaster :", response.text)
    
    
    

def main():
    podCaster()
    

def format_quests(items):
    if not items:
        return ''
    elif len(items) == 1:
        return items[0]
    elif len(items) == 2:
        return ' and '.join(items)
    else:
        return ', '.join(items[:-1]) + ', and ' + items[-1]



if __name__ == "__main__":
    main()
