import operator
import os
import subprocess
import sys
import PyPDF2
import instaloader
import pyttsx3
import speech_recognition as sr
import datetime
import psutil
import webbrowser
import datetime
import time
import pyautogui
import pywhatkit as kit
import platform
import random
import requests
from bs4 import BeautifulSoup
import subprocess
import ctypes
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier

# Database connection
import sqlite3
import insert_data  # Import the insert_query_data function from insert_data.py


from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvisUi import Ui_JarvisUi

# Initialize the text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# Text to Speech
def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()






# To wish with date and time
def wish():
    current_time = datetime.datetime.now()
    hour = current_time.hour
    date_str = current_time.strftime("%A, %B %d, %Y")
    time_str = current_time.strftime("%I:%M %p")

    if hour >= 0 and hour < 12:
        greeting = "Good Morning Sir"
    elif hour >= 12 and hour < 18:
        greeting = "Good Afternoon Sir"
    else:
        greeting = "Good Evening Sir"

    speak(f"{greeting}. Today is {date_str} and the time is {time_str}.")
    speak("I am Jarvis, your Personal AI Assistant. Please tell me how I can help you.")

# Open application function
def open_application(name, path):
    speak(f"Opening {name}.")
    os.startfile(path)

# Close application function
def close_application(name):
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() == name:
                speak(f"Closing {name}.")
                proc.terminate()
                return
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    speak(f"{name} is not open.")

# Switch window function
def switch_window():
    speak("Switching the window.")
    pyautogui.hotkey("alt", "tab")

# Fetch the latest news
def tell_news():
    speak("Fetching the latest news.")
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=a272a4c6e1c842bd8649b64f94bec8b2"
    response = requests.get(url).json()
    articles = response.get("articles", [])
    if articles:
        speak("Here are the top 5 latest news headlines.")
        for i, article in enumerate(articles[:5], 1):
            speak(f"News {i}: {article['title']}")
    else:
        speak("Sorry, I couldn't retrieve the news at the moment.")

 
# Location function
def find_phone_location(trace_number):
    try:
        # Parse the phone number
        ch_num = phonenumbers.parse(trace_number, "CH")  # CH for Country
        ser_num = phonenumbers.parse(trace_number, "RO")  # RO for Carrier

        # Get location and carrier information
        location = geocoder.description_for_number(ch_num, "en")  # Get location in English
        service_provider = carrier.name_for_number(ser_num, "en")  # Get carrier name

        return location, service_provider
    except Exception as e:
        return str(e)
    
# Fetchnig the Weather

def find_weather(location):
    """Find and return the weather for a given location using OpenWeatherMap API."""
    api_key = "f6bf4fdda7fb3dc8c60730af9c79e963"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    try:
        # Make the API request
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"  # For temperature in Celsius
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        if data["cod"] == 200:
            # Extract weather information
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            weather_info = f"{temp}°C with {description}"
            return weather_info
        else:
            return f"Error: {data['message']}"
    except Exception as e:
        return "Unable to fetch the weather. Please check your internet connection or try again."

 
# Tell a joke
def tell_joke():
    jokes = [
        "Why did the computer go to the doctor? Because it had a virus!",
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings!",
    ]
    joke = random.choice(jokes)
    speak(joke)

# Shut down the system
def shutdown_system():
    speak("Shutting down the system.")
    os.system("shutdown /s /t 1")

# Restart the system
def restart_system():
    speak("Restarting the system.")
    os.system("shutdown /r /t 1")

# Put the system to sleep
def sleep_system():
    speak("Putting the system to sleep.")
    if platform.system() == "Windows":
        ctypes.windll.powrprof.SetSuspendState(0, 1, 0)
    elif platform.system() == "Linux":
        os.system("systemctl suspend")
    else:
        speak("Sleep command not supported on this operating system.")

# Close application or browser tab function
def close_application(name):
    found = False
    for proc in psutil.process_iter():
        try:
            # Check for the browser process (adjust for your browser)
            if name.lower() in proc.name().lower():
                speak(f"Closing {name}.")
                proc.terminate()
                found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    if not found:
        speak(f"{name} is not currently open.")

# Use pyautogui to close the active browser tab
def close_browser_tab():
    speak("Closing the current browser tab.")
    pyautogui.hotkey("ctrl", "w")


class MainThread(QThread):

    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()

    # Take command: To convert voice to text
    def takeCommand(self):


            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 1
                audio = r.listen(source, timeout=10, phrase_time_limit=15)
            try:
                print("Recognizing...")
                self.query = r.recognize_google(audio, language='en-in')
                print(f"User said: {self.query}\n")
            except sr.WaitTimeoutError:
                print("Listening timed out, please try speaking again.")
                return "None"
            except Exception as e:
                print("Say that again please...")
                return "None"
            return self.query


    def TaskExecution(self):

        wish()

        while True:
            self.query = self.takeCommand().lower()

            # Logic for different tasks
            if "open notepad" in self.query:
                # open_application("notepad", "notepad.exe")
                # insert_data.insert_query_data(f"Weather query for {query}")
                open_application("notepad", "notepad.exe")
                result = f"Opened Notepad for the query: {self.query}"
                insert_data.insert_query_data(f"Notepad data stored {result}")
                speak("Notepad data is stored successfully...")
                
            elif "open cmd" in self.query:
                open_application("cmd", "cmd.exe")
                result = f"Opened cmd for the query: {self.query}"
                insert_data.insert_query_data(f"Command prompt data stored {result}")
                speak("Command prompt data is stored successfully...")
                

            elif "open youtube" in self.query:
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com")
                result = f"Opened Youtube for the query: {self.query}"
                insert_data.insert_query_data(f"Youtube data stored {result}")
                speak("Youtube data is stored successfully...")


            elif "open facebook" in self.query:
                speak("Opening Facebook")
                webbrowser.open("https://www.facebook.com")
                result = f"Opened facebook for the query: {self.query}"
                insert_data.insert_query_data(f"facebook data stored {result}")
                speak("Facebook data is stored successfully...")


            elif "open stack overflow" in self.query:
                speak("Opening Stack Overflow")
                webbrowser.open("https://stackoverflow.com")
                result = f"Opened Stack Overflow for the query: {self.query}"
                insert_data.insert_query_data(f"Stack Overflow data stored {result}")
                speak("Stack Overflow data is stored successfully...")


            elif "open google" in self.query:
                speak("Sir, what should I search in Google?")
                cm = self.takeCommand().lower()
                webbrowser.open(f"https://www.google.com/search?q={cm}")
                result = f"Opened Google for the query: {self.query}"
                insert_data.insert_query_data(f"Google data stored {result}")
                speak("Google data is stored successfully...")


            elif "play songs on youtube" in self.query:
                kit.playonyt("Believer")
            elif "track a phone number" in self.query:
                speak("Enter a mobile number whom you want to find?")
                trace_number = input("Enter the phone number (including country code, e.g., +91 for India): ").strip()

                if trace_number.startswith("+"):
                    location, provider = find_phone_location(trace_number)
                    if location and provider:
                        response = f"The location of the number is {location}, and the service provider is {provider}."
                    else:
                        response = "The phone number could not be processed. Please try again with a valid number."
                else:
                    response = "Please include the country code and try again."

                print(response)
                speak(response)
                result = f"Opened Tracking for the query: {self.query}"
                insert_data.insert_query_data(f"Tracking data stored {result}")
                speak("Tracking data is stored successfully...")
                
                        
            elif "take a screenshot" in self.query:
                try:
                    speak("Sir, please tell me the name for this screenshot file.")
                    name = self.takeCommand().lower().strip()  # Strip extra spaces
                    if not name or any(char in name for char in r'\/:*?"<>|'):  # Validate the filename
                        speak("The provided name is invalid or empty. Using a default name.")
                        name = f"screenshot_{int(time.time())}"  # Default name if invalid

                    # Ensure the file extension is correct
                    if not name.endswith(".png"):
                        name += ".png"

                    screenshot_path = os.path.join(os.getcwd(), name)

                    # Take and save the screenshot
                    speak("Please hold the screen steady. I am taking the screenshot.")
                    time.sleep(3)
                    img = pyautogui.screenshot()
                    img.save(screenshot_path)
                    speak(f"Screenshot saved as {screenshot_path}.")

                    result = f"Opened ScreenShot for the query: {self.query}"
                    insert_data.insert_query_data(f"ScreenShot data stored {result}")
                    speak("ScreenShot data is stored successfully...")
                except Exception as e:
                    speak("Sorry, I couldn't take the screenshot.")
                    print(f"Error: {e}")


            elif "do some calculations" in self.query or "can you calculate" in self.query:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    speak("Say what you want to calculate, example: 3 plus 3")
                    print("Listening...")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)

                try:
                    my_string = r.recognize_google(audio)
                    print(my_string)

                    def get_operator_fn(op):
                        return {
                            "+": operator.add,
                            "-": operator.sub,
                            "x": operator.mul,
                            "divided": operator.truediv  # Corrected method
                        }[op]

                    def eval_binary_expr(op1, oper, op2):
                        op1, op2 = int(op1), int(op2)
                        return get_operator_fn(oper)(op1, op2)

                    speak("Your result is: ")
                    speak(eval_binary_expr(*(my_string.split())))

                    result = f"Opened Math calculations for the query: {self.query}"
                    insert_data.insert_query_data(f"Notepad data stored {result}")
                    speak("Notepad data is stored successfully...")

                except Exception as e:
                    speak("I couldn't process your request. Please try again.")
                    print(f"Error: {e}")


            elif "who am i" in self.query:
                speak("You are Mr. Avinash and my master...")


            elif "who are you" in self.query:
                speak("I am Jarvis, your Personal AI Assistant. Please tell me how I can help you.")

            elif "hello jarvis" in self.query or "hey jarvis" in self.query:
                speak("Hello Sir, may I help you with something")

            elif "how are you" in self.query:
                speak("I am good. What about you?")
            elif "i am good" in self.query or "i am fine" in self.query or "i'm fine" in self.query:
                speak("That's great to hear from you.")
            elif "thank you" in self.query or "thanks" in self.query:
                speak("It's my pleasure, Sir.")
            
            elif "what is today's date" in self.query or "what's today's date" in self.query:
                from datetime import datetime  # Ensure proper import
                now = datetime.now()
                current_date = now.strftime("%B %d, %Y")
                current_time = now.strftime("%I:%M %p")
                speak(f"Today's date is {current_date} and the current time is {current_time}.")
                result = f"Opened DateInfo for the query: {self.query}"
                insert_data.insert_query_data(f"DateInfo data stored {result}")
                speak("DateInfo data is stored successfully...")


        
        
            elif "find the weather" in self.query:
                speak("Enter the location to find the weather")
                location = input("Enter the location to find the weather: ").strip()
                weather_info = find_weather(location)

                print(f"Weather in {location}: {weather_info}")
                speak(f"The weather in {location} is {weather_info}")
                result = f"Opened Weather for the query: {self.query}"
                insert_data.insert_query_data(f"Weather data stored {result}")
                speak("Weather data is stored successfully...")


            # Inside your TaskExecution method
            elif "what can you do" in self.query:
                speak("""
                I can help with many things! Here's what I can do for you:
                1. Assist with programming tasks and debugging code.
                2. Provide explanations and examples for algorithms and data structures.
                3. Help with project ideas, documentation, and planning.
                
                Feel free to ask me anything, and I'll do my best to assist you!
                """)

            elif "send mail" in self.query or "send email" in self.query:
            
                 # Prompt for sender email
                 
                email = "d.avinashkumar22@gmail.com"

                # Prompt for receiver email
                speak("Enter receiver's email address ")
                receiver_email = input("Enter receiver's email address: ")

                # Prompt for subject
                speak("Enter the email subject")
                subject = self.takeCommand()

                # Prompt for message body
                speak("Enter your message: ")
                message = self.takeCommand()

                # Format the email text
                text = f"Subject: {subject}\n\n{message}"

                # SMTP configuration
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()

                try:
                    # Login to the SMTP server
                    server.login(email, "dyls ombd uyfc ncuu")

                    # Send the email
                    server.sendmail(email, receiver_email, text)
                    speak("Mail sent successfully!")
                    print("Mail sent successfully!")
                    result = f"Opened Email for the query: {self.query}"
                    insert_data.insert_query_data(f"Email data stored {result}")
                    speak("Email data is stored successfully...")
                except Exception as e:
                    speak("Failed to send email")
                    print(f"Failed to send email: {e}")
                finally:
                    server.quit()


            elif "switch the window" in self.query:
                switch_window()
                result = f"Opened Tab switch for the query: {self.query}"
                insert_data.insert_query_data(f"Tab switch data stored {result}")
                speak("Tab switch data is stored successfully...")


            elif "tell me the latest news" in self.query:
                tell_news()
                result = f"Opened New Inforamtion for the query: {self.query}"
                insert_data.insert_query_data(f"New Inforamtion data stored {result}")
                speak("New Inforamtion data is stored successfully...")
             
            elif "tell me a joke" in self.query:
                tell_joke()   
                result = f"Opened Jokes for the query: {self.query}"
                insert_data.insert_query_data(f"Jokes data stored {result}")
                speak("Jokes data is stored successfully...")


            
            elif "close notepad" in self.query:
                close_application("notepad.exe")
            elif "close command prompt" in self.query:
                close_application("cmd.exe")
            
            elif "shutdown the system" in self.query:
                shutdown_system()
                break
            elif "restart the system" in self.query:
                restart_system()
                break
            elif "sleep the system" in self.query:
                sleep_system()

            elif "close youtube" in self.query:
                close_browser_tab()

            elif "close facebook" in self.query:
                close_browser_tab()

            elif "close stack overflow" in self.query:
                close_browser_tab()


            elif "close browser" in self.query:
                close_application("chrome")  # Or the name of the browser you use, e.g., "firefox", "edge"


            elif "exit" in self.query or "quit" in self.query:
                speak("Goodbye Sir.")
                break
                
            elif "you can sleep" in self.query or "sleep now" in self.query:
                speak("Okay Sir, I am going to sleep you can call me anytime")
                break

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_JarvisUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)
    
    def startTask(self):
        self.ui.movie = QtGui.QMovie("../NewJarvis/GUI/ironman.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie = QtGui.QMovie("../NewJarvis/GUI/jarvis.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(5000)
        startExecution.start()

    def showTime(self):

        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString("hh:mm:ss")
        label_data = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_data)
        self.ui.textBrowser_2.setText(label_time)

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())