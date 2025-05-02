import re
from assistant.voice_recognition import recognize_speech
from assistant.nlp_processing import parse_command
from assistant.text_to_speech import speak
from assistant.commands import system_controls, media_controls, web_search, system_info, alarm_reminder

class VoiceAssistant:
    def __init__(self, output_callback=None):
        self.running = True
        self.output_callback = output_callback  # For GUI updates

    def run(self):
        self._respond("Hello! How can I assist you today?")
        while self.running:
            command = recognize_speech()
            if command:
                self._respond(f"You said: {command}")
                action, details = parse_command(command)
                self.handle_command(action, details)

    def handle_command(self, action, details):
        if action == 'open_application':
            app_name = details.split()[-1]
            self._respond(f"Opening {app_name}")
            system_controls.open_application(app_name)

        elif action == 'play_media':
            media_name = details.replace('play', '', 1).strip()
            self._respond(f"Playing {media_name}")
            media_controls.play_media(media_name)

        elif action == 'web_search':
            query = details.replace('search', '', 1).strip()
            self._respond(f"Searching for {query}")
            result = web_search.wikipedia_summary(query)
            self._respond(result)

        elif action == 'set_volume':
            match = re.search(r'\d+', details)
            if match:
                level = int(match.group())
                self._respond(f"Setting volume to {level}%")
                system_controls.set_volume(level)
            else:
                self._respond("Please tell me the volume level, like 70 percent.")

        elif action == 'set_brightness':
            match = re.search(r'\d+', details)
            if match:
                level = int(match.group())
                self._respond(f"Setting brightness to {level}%")
                system_controls.set_brightness(level)
            else:
                self._respond("Please tell me the brightness level, like 50 percent.")

        elif action == 'how_are_you':
            self._respond("I'm doing great! How about you?")

        elif action == 'time':
            time_message = system_controls.tell_time()
            self._respond(time_message)

        elif action == 'date':
            date_message = system_controls.tell_date()
            self._respond(date_message)

        elif action == 'system_info':
            info = system_info.get_system_info()
            self._respond(info)

        elif action == 'set_alarm':
            response = alarm_reminder.set_alarm(details)
            self._respond(response)

        elif action == 'exit':
            self._respond("Goodbye! Shutting down.")
            self.running = False

        elif action == 'unknown':
            self._respond("I'm not sure how to help with that.")

    def _respond(self, message):
        """Speak and send response to GUI (if attached)."""
        speak(message)
        if self.output_callback:
            self.output_callback(message)

    def listen(self):
        return recognize_speech()
