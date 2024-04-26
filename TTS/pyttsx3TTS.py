import pyttsx3


class Pyttsx3TTS:
    def get_tts_audio(self, text):
        engine = pyttsx3.init()

        engine.setProperty('rate', 150)  # Speed percent (can go over 100).
        engine.setProperty('volume', 0.8)  # Volume 0-1.
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  # 0 = female voice, 1 = male voice.

        engine.say(text)
        engine.runAndWait()
