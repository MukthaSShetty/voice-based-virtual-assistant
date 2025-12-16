import tkinter as tk
from tkinter import Frame, Label, Entry, Button, Text, Scrollbar, END
import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import requests
import os
from datetime import datetime
import pyautogui  # For taking screenshots
import random

# Initialize text-to-speech engine
engine = pyttsx3.init()


# Speak function
def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()


# Listen function
def listen():
    """Listen to the user's voice and return the text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Speech recognition service is unavailable."


# Weather function
def get_weather(city):
    """Fetch weather information for a given city."""
    api_key = "your_openweathermap_api_key"  # Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url).json()
        if response.get("cod") != 200:
            return "Couldn't fetch the weather details."
        weather = response["weather"][0]["description"]
        temp = response["main"]["temp"]
        return f"The weather in {city} is {weather} with a temperature of {temp}°C."
    except:
        return "Couldn't fetch the weather details."


# Joke function
def tell_joke():
    """Tell a random joke."""
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why don’t oysters donate to charity? Because they are shellfish.",
        "I told my computer I needed a break, and it froze."
    ]
    return random.choice(jokes)


# Additional Commands
def open_calculator():
    """Open the calculator application."""
    os.system("calc")
    return "Opening calculator."


def open_notepad():
    """Open the Notepad application."""
    os.system("notepad")
    return "Opening Notepad."


def take_screenshot():
    """Take a screenshot and save it."""
    screenshot = pyautogui.screenshot()
    filename = datetime.now().strftime("screenshot_%Y-%m-%d_%H-%M-%S.png")
    screenshot.save(filename)
    return f"Screenshot taken and saved as {filename}."


def get_date():
    """Get the current date."""
    today = datetime.now().strftime("%A, %B %d, %Y")
    return f"Today's date is {today}."


# Process command function
def process_command(command):
    """Process the user's command and return the response."""
    if "play" in command:
        song = command.replace("play", "").strip()
        pywhatkit.playonyt(song)
        return f"Playing {song} on YouTube."
    elif "time" in command:
        now = datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}."
    elif "date" in command:
        return get_date()
    elif "search" in command:
        query = command.replace("search", "").strip()
        pywhatkit.search(query)
        return f"Searching for {query} online."
    elif "who is" in command or "what is" in command:
        query = command.replace("who is", "").replace("what is", "").strip()
        return wikipedia.summary(query, sentences=2)
    elif "weather" in command:
        return "Please enter a city name in the text box."
    elif "calculator" in command:
        return open_calculator()
    elif "notepad" in command:
        return open_notepad()
    elif "screenshot" in command:
        return take_screenshot()
    elif "joke" in command:
        return tell_joke()
    elif "goodbye" in command:
        speak("Goodbye! Have a great day!")
        root.destroy()
        return "Goodbye!"
    else:
        return "I'm not sure how to do that, but I'm learning."


# GUI functions
def handle_command(command):
    """Handle the command entered or spoken by the user."""
    output_text.insert(END, f"You: {command}\n")

    if "weather" in command:
        city = listen()
        response = get_weather(city)
    else:
        response = process_command(command)

    speak(response)
    output_text.insert(END, f"Assistant: {response}\n")


# Continuous listening function
def listen_and_process():
    """Listen continuously and process commands."""
    while True:
        speak("Listening...")
        command = listen()
        if command:
            handle_command(command)


# Enhanced GUI Design
root = tk.Tk()
root.title("Advanced Voice Assistant")
root.geometry("600x700")
root.config(bg="#1e1e2f")  # Background color

# Frames for Layout
header_frame = Frame(root, bg="#282c34", height=100)
header_frame.pack(fill="x")

input_frame = Frame(root, bg="#3e4451", height=80)
input_frame.pack(fill="x", pady=10)

output_frame = Frame(root, bg="#21252b")
output_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Header Section
header_label = Label(
    header_frame,
    text="Advanced Voice Assistant",
    font=("Helvetica", 24, "bold"),
    fg="#61dafb",
    bg="#282c34",
)
header_label.pack(pady=20)

# Output Section
output_label = Label(
    output_frame, text="Conversation:", font=("Arial", 14), fg="white", bg="#21252b"
)
output_label.pack(anchor="nw", pady=5)

scrollbar = Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")

output_text = Text(
    output_frame,
    font=("Arial", 12),
    bg="#2c313a",
    fg="white",
    wrap="word",
    yscrollcommand=scrollbar.set,
)
output_text.pack(fill="both", expand=True, padx=5, pady=5)
scrollbar.config(command=output_text.yview)

# Start with a welcome message
speak("I'm your voice assistant. How can I assist you today?")

# Start listening and processing commands in the background
import threading

threading.Thread(target=listen_and_process, daemon=True).start()

# Run the application
root.mainloop()