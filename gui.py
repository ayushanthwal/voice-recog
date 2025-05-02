
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QMovie, QIcon
from assistant.assistant import VoiceAssistant
from assistant.voice_recognition import recognize_speech
from assistant.text_to_speech import speak
from assistant.nlp_processing import parse_command
import sys
import psutil
import datetime

class VoiceAssistantThread(QThread):
    update_text = Signal(str)
    exit_signal = Signal()

    def __init__(self):
        super().__init__()
        # ✅ Pass the output callback to VoiceAssistant
        self.assistant = VoiceAssistant(output_callback=self.update_text.emit)
        self.running = True

    def run(self):
        self.assistant.running = True
        self.update_text.emit("Assistant is listening...")
        speak("Assistant is listening...")
        while self.assistant.running and self.running:
            command = recognize_speech()
            if command:
                self.update_text.emit(f"You said: {command}")
                action, details = parse_command(command)

                if action == "system_info":
                    info = self.get_system_info()
                    self.update_text.emit(info)
                    speak(info)

                elif action == "set_alarm":
                    response = self.set_alarm(details)
                    self.update_text.emit(response)
                    speak(response)

                elif action != "exit":
                    self.assistant.handle_command(action, details)

                else:
                    self.assistant.handle_command(action, details)
                    self.exit_signal.emit()

    def stop(self):
        self.running = False
        self.assistant.running = False
        self.quit()
        self.wait()

    def get_system_info(self):
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        return f"CPU Usage: {cpu}%, RAM Usage: {ram}%"

    def set_alarm(self, time_text):
        try:
            now = datetime.datetime.now()
            alarm_time = datetime.datetime.strptime(time_text.strip(), "%H:%M")
            alarm_time = now.replace(hour=alarm_time.hour, minute=alarm_time.minute, second=0, microsecond=0)
            if alarm_time < now:
                alarm_time += datetime.timedelta(days=1)
            QTimer.singleShot(int((alarm_time - now).total_seconds() * 1000), self.trigger_alarm)
            return f"Alarm set for {alarm_time.strftime('%H:%M')}"
        except ValueError:
            return "Please provide time in HH:MM format."

    def trigger_alarm(self):
        msg = "⏰ Alarm time reached!"
        self.update_text.emit(msg)
        speak(msg)

class VoiceAssistantApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Assistant GUI")
        self.setFixedSize(460, 580)
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-size: 16px;")
        self.setWindowIcon(QIcon("assets/mic_icon.png"))

        layout = QVBoxLayout()

        self.status_label = QLabel("🎤 Click the button to start speaking")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(self.status_label)

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("background-color: #2e2e2e; border: none; padding: 10px;")
        layout.addWidget(self.output_area)

        self.animation_label = QLabel()
        self.movie = QMovie("assets/mic_wave.gif")
        self.animation_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.animation_label)
        self.movie.setScaledSize(self.animation_label.size())

        button_layout = QHBoxLayout()
        self.listen_button = QPushButton("🎤 Start Listening")
        self.listen_button.clicked.connect(self.toggle_listening)
        self.listen_button.setStyleSheet("""
            padding: 12px;
            font-weight: bold;
            background-color: #00b894;
            color: white;
            border-radius: 12px;
        """)
        button_layout.addWidget(self.listen_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.assistant_thread = VoiceAssistantThread()
        self.assistant_thread.update_text.connect(self.update_output)
        self.assistant_thread.exit_signal.connect(self.close_app)
        self.listening = False

    def toggle_listening(self):
        if not self.listening:
            self.listen_button.setText("⏹️ Stop Listening")
            self.status_label.setText("🔊 Listening...")
            self.movie.start()
            self.animation_label.setMovie(self.movie)
            self.assistant_thread.start()
        else:
            self.listen_button.setText("🎤 Start Listening")
            self.status_label.setText("🎤 Click the button to start speaking")
            self.movie.stop()
            self.animation_label.clear()
            self.assistant_thread.stop()

        self.listening = not self.listening

    def update_output(self, message):
        self.output_area.append(message)

    def close_app(self):
        self.output_area.append("Shutting down assistant...")
        QTimer.singleShot(2000, self.close)

def run_gui_app():
    app = QApplication(sys.argv)
    window = VoiceAssistantApp()
    window.show()
    sys.exit(app.exec())
