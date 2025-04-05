import re

def parse_command(command):
    """Parse the user's command and determine the intent."""
    command = command.lower()
    
    if re.search(r'\b(bye|goodbye|exit|stop|shutdown|shut down|quit)\b', command):
        return 'exit', command
    elif re.search(r'\b(open|start|launch)\b', command):
        return 'open_application', command
    elif re.search(r'\b(play)\b', command):
        return 'play_media', command
    elif re.search(r'\b(search)\b', command):
        return 'web_search', command
    elif re.search(r'\b(set volume|increase volume|decrease volume)\b', command):
        return 'set_volume', command
    elif re.search(r'\b(set brightness|increase brightness|decrease brightness)\b', command):
        return 'set_brightness', command
    else:
        return 'unknown', command
