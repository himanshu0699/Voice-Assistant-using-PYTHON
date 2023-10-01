import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
import random
from config import apikey
import numpy as np
import win32com.client
import subprocess

# Initialize an empty string to store the conversation history
chatStr = ""

# Function to send a message and get a response
def chat(query):
    global chatStr
    print(chatStr)

    # Set the OpenAI API key
    openai.api_key = apikey

    # Create a message in the required format
    message = {
        "role": "user",
        "content": query
    }

    # Append the user's message to the conversation history
    chatStr += f"user: {query}\n"

    # Create a list of messages for the API request
    messages = [{"role": "system", "content": f"{query}"}]
    messages.append(message)

    # Make the API request
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract and return Nova's response
    nova_response = response["choices"][0]["message"]["content"]
    say(nova_response)
    chatStr += f"Nova: {nova_response}\n"
    return nova_response

# Function to generate AI response and save it to a file
def ai(prompt):
    openai.api_key = apikey

    # Create a message in the required format
    message = {
        "role": "user",
        "content": prompt
    }

    # Create a list of messages for the API request
    messages = [{"role": "system", "content": f"{prompt}"}]
    messages.append(message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract Nova's response
    nova_response = response["choices"][0]["message"]["content"]

    # Prepare the response text
    text = f"OpenAI response for Prompt: {prompt}\n *************************\n\n{nova_response}"

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)

    return nova_response

def say(text):
    speaker = win32com.client.Dispatch("SAPI.Spvoice")
    speaker.speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.start_threshold = 0.2
        r.pause_threshold =  1.5
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Nova"

task_done = False
if __name__ == '__main__':
    print('Welcome to Nova A.I')
    say("Welcome to Nova AI")
    while True:
        print("Listening...")
        query = takeCommand()
        query = query.lower()

        
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                task_done = True

        if "play music" in query:
            musicPath = r"C:\Users\Himanshu\Music\hy.mp3"
            os.system(f"start {musicPath}")
            task_done = True


        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} and {min} minutes")
            task_done = True


        elif "open spotify".lower() in query.lower():
            subprocess.Popen([r"C:\Users\Himanshu\AppData\Roaming\Spotify\Spotify"])
            task_done = True


        elif "open chrome".lower() in query.lower():
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            subprocess.Popen([chrome_path])
            task_done = True


        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
            task_done = True


        elif "Nova Quit".lower() in query.lower():
            exit()

        elif "reset the chat".lower() in query.lower():
            global ChatStr  # Declare chatStr as global
            chatStr = ""
        
        elif len(query) == 0:
            task_done = True
            continue
            
            

        if task_done != True:
            print("Nova is thinking...")
            chat(query)
