import whisper
import speech_recognition as sr
import tempfile
import os
from pydub import AudioSegment
import io


class SpeechRecognition:
    def __init__(self, model="tiny", inMemory=True, english=True, energyThreshold=500, dynamicEnergy=True, pause=1.2, verbose=False):
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
        self.english = english
        if model != "large" and english:
            model = model + ".en"
            self.model = whisper.load_model(model, in_memory=inMemory)
        else:
            self.model = whisper.load_model(model, in_memory=inMemory)
        self.dynamicEnergy = dynamicEnergy
        self.pause = pause
        self.verbose = verbose
        self.energyThreshold = energyThreshold
        self.tempDir = tempfile.mkdtemp()
        self.savePath = os.path.join(self.tempDir, "temp.wav")

    def ListenAndTranscribe(self):
        with self.mic as source:
            try:
                self.r.adjust_for_ambient_noise(source)
                print("Started Listening")
                audio = self.r.listen(source)
                data = io.BytesIO(audio.get_wav_data())
                audio_clip = AudioSegment.from_file(data)
                audio_clip.export(self.savePath, format="wav")
                print("Stopped Listening")
            except:
                print("Error")
                return "Error"
            try:
                if self.english:
                    print("Transcribing")
                    result = self.model.transcribe(
                        self.savePath, language="english")
                else:
                    print("Transcribing")
                    result = self.model.transcribe(self.savePath)
                if not self.verbose:
                    predicted_text = result["text"]
                    print(f"Transcription: {predicted_text}")
                else:
                    predicted_text = result
                    print(f"Transcription: {predicted_text}")
            except:
                predicted_text = "Error: Could not transcribe audio"
        return predicted_text