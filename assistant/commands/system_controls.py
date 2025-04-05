# assistant/commands/system_controls.py
import os
import subprocess
from assistant.text_to_speech import speak

def open_application(app_name):
    """Open an application by name."""
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen([app_name])
        elif os.name == 'posix':  # macOS, Linux
            subprocess.Popen(['open', '-a', app_name])
        speak(f"Opening {app_name}.")
    except Exception as e:
        speak(f"Failed to open {app_name}: {e}")

def set_volume(level):
    """Set the system volume to the specified level."""
    # Implementation depends on the operating system
    speak(f"Setting volume to {level}%.")
    # Add OS-specific code here

def set_brightness(level):
    """Set the screen brightness to the specified level."""
    # Implementation depends on the operating system and hardware
    speak(f"Setting brightness to {level}%.")
    # Add OS-specific code here
