import openai
import os
import speech_recognition as sr
import requests
import pyttsx3
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Speech Engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "I didn't understand that."
    except sr.RequestError:
        return "API unavailable."

def get_ai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def get_weather(city="New York"):
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url).json()
    return f"The weather in {city} is {response['current']['condition']['text']} with a temperature of {response['current']['temp_c']}°C."

# Main Loop
if __name__ == "__main__":
    speak("Hello! How can I assist you?")
    while True:
        command = listen()
        if command.lower() in ["exit", "quit"]:
            speak("Goodbye!")
            break
        response = get_ai_response(command)
        print(f"AI: {response}")
        speak(response)
