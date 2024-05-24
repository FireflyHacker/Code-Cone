import pyttsx4
from threading import Thread

class _TTS:
    engine = None
    rate = None

    def __init__(self):
        self.engine = pyttsx4.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 150)  # setting up new voice rate

    def start(self, text_):
        thread = Thread(target=self.speak(text_))
        thread.start()

    def speak(self, text_):
        self.engine.say(text_)
        self.engine.runAndWait()

    def save(self, text_, path_):
        self.engine.save_to_file(text_, path_)
        self.engine.runAndWait()
