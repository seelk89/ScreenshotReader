from TTS.pyttsx3TTS import Pyttsx3TTS

import time
import threading


class StringWatcherAndReader(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            value = self.queue.get()

            if value is not None and isinstance(value, str):
                string_to_audio(value)
            time.sleep(1)  # Sleep for performance.

    def stop(self):
        self.stop_event.set()


def string_to_audio(string):
    tts = Pyttsx3TTS()
    tts.get_tts_audio(string)
