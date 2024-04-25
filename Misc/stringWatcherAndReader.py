from TTS.pyttsx3TTS import Pyttsx3TTS

import time
import threading


class StringWatcherAndReader(threading.Thread):
    def __init__(self, variable):
        super().__init__()
        self.variable = variable
        self.stop_event = threading.Event()
        self.previous_value = None

    def run(self):
        while not self.stop_event.is_set():
            if (
                self.variable.has_changed()
                and self.variable.value != self.previous_value
            ):
                self.previous_value = self.variable.value
                if isinstance(self.variable.value, str):
                    # print(self.variable.value)
                    string_to_audio(self.variable.value)
            time.sleep(1)

    def stop(self):
        self.stop_event.set()


def string_to_audio(string):
    tts = Pyttsx3TTS()
    tts.get_tts_audio(string)
