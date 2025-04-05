# assistant/main.py
import sys
import os
from assistant.assistant import VoiceAssistant


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))




def main():
    assistant = VoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()
