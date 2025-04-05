import re
from assistant.voice_recognition import recognize_speech
from assistant.nlp_processing import parse_command
from assistant.text_to_speech import speak
from assistant.commands import system_controls, media_controls, web_search

class VoiceAssistant:
    def __init__(self):
        self.running = True

    def run(self):
        speak("Hello! How can I assist you today?")
        while self.running:
            command = recognize_speech()
            if command:
                action, details = parse_command(command)
                self.handle_command(action, details)

    def handle_command(self, action, details):
        if action == 'open_application':
            app_name = details.split()[-1]
            system_controls.open_application(app_name)

        elif action == 'play_media':
            media_name = details.replace('play', '', 1).strip()
            media_controls.play_media(media_name)

        elif action == 'web_search':
            query = details.replace('search', '', 1).strip()
            web_search.search(query)

        elif action == 'set_volume':
            match = re.search(r'\d+', details)
            if match:
                level = int(match.group())
                system_controls.set_volume(level)
            else:
                speak("Please tell me the volume level, like 70 percent.")

        elif action == 'set_brightness':
            match = re.search(r'\d+', details)
            if match:
                level = int(match.group())
                system_controls.set_brightness(level)
            else:
                speak("Please tell me the brightness level, like 50 percent.")

        elif action == 'greeting':
            speak("I'm doing great! How about you?")

        elif action == 'time':
            system_controls.tell_time()

        elif action == 'date':
            system_controls.tell_date()

        elif action == 'exit':
            speak("Goodbye! Shutting down.")
            self.running = False

        elif action == 'unknown':
            speak("I'm not sure how to help with that.")
            
        elif action == 'exit':
            speak("Goodbye! Shutting down.")
            self.running = False

