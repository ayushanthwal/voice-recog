import re
import string

def tokenize(text):
    """Simple tokenizer that splits text into lowercase words, removing punctuation."""
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    return tokens

def parse_command(command):
    """Parse the user's command and determine the intent."""
    tokens = tokenize(command)
    command_lower = ' '.join(tokens)

    if any(word in tokens for word in ['bye', 'goodbye', 'exit', 'stop', 'shutdown', 'quit']):
        return 'exit', command
    elif any(word in tokens for word in ['open', 'start', 'launch']):
        return 'open_application', command
    elif 'play' in tokens:
        return 'play_media', command
    elif 'search' in tokens:
        return 'web_search', command
    elif any(phrase in command_lower for phrase in ['set volume', 'increase volume', 'decrease volume']):
        return 'set_volume', command
    elif any(phrase in command_lower for phrase in ['set brightness', 'increase brightness', 'decrease brightness']):
        return 'set_brightness', command
    elif 'how are you' in command_lower or 'how r you' in command_lower:
        return 'how_are_you', command
    else:
        return 'unknown', command
