import os
import speech_recognition as sr
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import numpy as np
from openai import OpenAI
import whisper


class AudioInterface:
    def __init__(self):
        self.client_elabs = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

        self.model = whisper.load_model("turbo", device="cuda")
        self.recognizer = sr.Recognizer()

    def listen(self) -> str:
        with sr.Microphone() as source:
            print("\n***Say something!")
            audio = self.recognizer.listen(source)
            self.save_recording(audio)
            result = self.model.transcribe("file.wav")
            return result["text"]

        # return self.transcribe("file.wav")

    def save_recording(self, audio):
        with open("file.wav", "wb") as f:
            f.write(audio.get_wav_data())

    def speak(self, text):
        audio = self.client_elabs.generate(
            text=text,
            voice="Laura",
            model="eleven_multilingual_v2",  # eleven_turbo_v2_5
            stream=True,
        )
        play(audio)
