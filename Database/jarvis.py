import pyttsx3
import datetime
import sqlite3
import requests
from datetime import datetime
import insert_data  # Import the insert_query_data function from insert_data.py

# Your function to speak the assistant's response
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Example query execution functions
def find_weather(query):
    # Simulate weather query processing
    speak(f"Searching for weather in {query}...")
    # After executing, insert this into the database
    insert_data.insert_query_data(f"Weather query for {query}")
    return f"Weather details for {query}"

def find_location(query):
    # Simulate location query processing
    speak(f"Finding location of {query}...")
    # After executing, insert this into the database
    insert_data.insert_query_data(f"Location query for {query}")
    return f"Location details for {query}"

# Main function to process commands
def process_query(query):
    if "weather" in query:
        result = find_weather(query)
    elif "location" in query:
        result = find_location(query)
    else:
        result = "Sorry, I didn't understand that query."
    
    speak(result)

# Example of user query
if __name__ == "__main__":
    user_query = input("How can I assist you? ")
    process_query(user_query)
