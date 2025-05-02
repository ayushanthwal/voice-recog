#Assistant/commands/web_search.py

import webbrowser
import wikipedia
from assistant.text_to_speech import speak

def search(query):
    speak(f"Searching the web for {query}")
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Your query is too vague. Did you mean: {', '.join(e.options[:3])}?"
    except wikipedia.exceptions.PageError:
        return "I couldn't find any information on that topic."
    except Exception as e:
        return f"An error occurred: {str(e)}"
