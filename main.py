
"""
KEVI-A Personal Linux Assistant:
    -KEVI is a linux assistant that controls your linux computer with voice commands.
    This program is the modification of the 'JARVIS' program by "Mohammed Shokr <mohammedshokr2014@gmail.com>",
    which controlled the windows program through voice commands. 

"""

__author__ = "Kabin Ghimire <ghimirekabin060@gmail.com>"
__version__ = "v 1.0"



# import modules
import datetime  
import subprocess  
import pyjokes # for generating random jokes
import requests
import json
from PIL import Image, ImageGrab
from pynput import keyboard
from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Controller
from playsound import *  # for sound output
import webbrowser
import smtplib
from groq import Groq
import speech_recognition as sr
import os



class KEVI:
    def __init__(self):
        self.exit_jarvis=False

    def printScr(self,text):
        print(text)


    def deliver_news(self):
        self.url = "https://newsapi.org/v2/everything?domains=wsj.com&apiKey=7d4803bfcad04530ae4c0d3b0eabe202"
        self.news = self.requests.get(self.url).text
        self.news_dict = self.json.loads(self.news)
        self.arts = self.news_dict["articles"]
        for index, articles in enumerate(self.arts):
            self.printScr(articles["title"])
            if index == len(self.arts) - 1:
                break
            self.printScr("Moving on the next news headline..")
        self.printScr("These were the top headlines, Have a nice day Sir!!..")


    def sendEmail(self,to, content):
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.login("ghimskewal@gmail.com", "kewal@12345")
        self.server.sendmail("ghimskewal@gmail.com",to,content)
        self.server.close()


    def ask_groq(self,que):
        self.client = Groq()
        self.que=que
        self.response_content = ""
        self.client = Groq()  
        self.answer = self.client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": f"answer this {self.que}"
            },
            {
                "role": "user",
                "content": ""
            },
            {
                "role": "assistant",
                "content": ""
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        )

        
        for chunk in self.answer:
            chunk_content = chunk.choices[0].delta.content or ""
            self.response_content += chunk_content
    
        
        return self.response_content


    # obtain audio from the microphone
    def takecommand(self):
        self.r =sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            self.r.pause_threshold = 1
            self.r.dynamic_energy_threshold = 500
            self.audio = self.r.listen(source)
        try:
            print("Recognizing...")
            self.query = self.r.recognize_google(self.audio, language="en-in")
            print(f"User said {self.query}\n")
        except Exception as e:
            print("Say that again please...")
            return "None"
        
        return self.query


    def controller_app(self,query):
        self.current = Controller()
        if query == "time":
            print(datetime.now())
        elif query == "news":
            self.deliver_news()
        elif query == "open sublime text":
            subprocess.call(["subl"])  # Ensure Sublime Text is installed and in PATH
        elif query == "open calculator":
            subprocess.call(["gnome-calculator"])  # For GNOME. Use "kcalc" for KDE, or "qalculate-gtk"
        elif query == "open terminal":
            subprocess.call(["alacritty"])  # Replace with your preferred terminal (e.g., konsole, gnome-terminal, xterm)
        elif query == "open browser":
            subprocess.call(["xdg-open", "https://www.google.com"])  # Opens the default browser
        elif query == "open youtube":
            webbrowser.open("https://www.youtube.com/") 
        elif query == "open google":
            webbrowser.open("https://www.google.com/")
        elif query == "open github":
            webbrowser.open("https://github.com/kabin007")
        elif query== "search for":
            self.que=query.lstrip("search for")
            answer = self.ask_groq(self.que)
            self.printScr(answer)
           
        elif query == "send me a mail":
            try:
                self.printScr("Please enter the details in the terminal below")
                self.to = input("Enter recepient email")
                self.content = input("Enter content")
                self.sendEmail(self.to, self.content)
                self.printScr(f"Email has been sent to {self.to} successfully!")
            except Exception as e:
                print(e)
                self.printScr("Sorry, I can't send the email.")
        elif query == "Jokes":
            self.printScr(pyjokes.get_joke())
        elif query== "take a break":
            exit()
        else:
            self.answer =self.ask_groq(query)
            self.printScr(self.answer)





if __name__ == "__main__":
    kevi=KEVI()
    while not kevi.exit_jarvis:
        Query = kevi.takecommand().lower()
        kevi.controller_app(Query)
    kevi.exit_jarvis = True
