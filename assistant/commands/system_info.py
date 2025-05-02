import platform
import psutil
from assistant.text_to_speech import speak

def get_system_info():
    info = {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "RAM": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"
    }
    
    summary = f"You are running {info['System']} on a {info['Processor']} processor with {info['RAM']} RAM."
    speak(summary)
    print(summary)
