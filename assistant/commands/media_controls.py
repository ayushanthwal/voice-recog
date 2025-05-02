# assistant/commands/media_controls.py

import pywhatkit
from assistant.text_to_speech import speak

def play_media(query):
    try:
        speak(f"Playing {query} on YouTube.")
        print(f"Playing {query} on YouTube...")
        pywhatkit.playonyt(query)
    except Exception as e:
        speak("Sorry, I couldn't play that video.")
        print(f"Error in play_media: {e}")
