# main.py
import sys
import os

# Add the assistant folder to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'assistant')))

from assistant.assistant import VoiceAssistant

def run_console():
    assistant = VoiceAssistant()
    assistant.run()

def run_gui():
    from gui import run_gui_app
    run_gui_app()

def main():
    mode = input("Enter mode (voice/gui): ").strip().lower()
    if mode == "gui":
        run_gui()
    else:
        run_console()

if __name__ == "__main__":
    main()
