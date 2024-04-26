from TTS.pyttsx3TTS import Pyttsx3TTS

import time
import threading


class StringWatcherAndReader(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.stop_event = threading.Event()
        self.previous_value = None

    def run(self):
        while not self.stop_event.is_set():
            # Get the value from the queue
            value = self.queue.get()

            # Check if the value is not None and different from the previous value
            if value is not None and value != self.previous_value:
                self.previous_value = value
                # Check if the value is a string
                if isinstance(value, str):
                    # Perform the desired action, e.g., string_to_audio
                    string_to_audio(value)
            # Sleep for some time before checking the queue again
            time.sleep(1)

    def stop(self):
        # Set the stop event to stop the thread
        self.stop_event.set()


def string_to_audio(string):
    tts = Pyttsx3TTS()
    tts.get_tts_audio(string)
