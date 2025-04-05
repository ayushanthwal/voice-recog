import webbrowser
from assistant.text_to_speech import speak

def search(query):
    speak(f"Searching the web for {query}")
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
