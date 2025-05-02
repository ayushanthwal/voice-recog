# assistant/commands/alarm_reminder.py

import datetime
import time
from threading import Thread



from assistant.text_to_speech import speak

def set_alarm(alarm_time):
    try:
        alarm_time_obj = datetime.datetime.strptime(alarm_time, "%H:%M").time()
    except ValueError:
        speak("Sorry, I couldn't understand the time format. Use HH:MM format.")
        return

    def alarm_thread():
        speak(f"Alarm set for {alarm_time_obj.strftime('%I:%M %p')}")
        while True:
            now = datetime.datetime.now().time() 
            if now.hour == alarm_time_obj.hour and now.minute == alarm_time_obj.minute:
                speak("It's time! Your alarm is ringing.")
                break
            time.sleep(20)

    Thread(target=alarm_thread, daemon=True).start()
