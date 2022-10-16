import requests
from pygame import mixer
import time
import os


class SpeechSynthesis:
    def __init__(self, text2BeSpoken):
        self.text2BeSpoken = text2BeSpoken
        self.API_KEY = "0sww17AF6iXk8lbmRtx25dYWceuY6kf1"
        self.PATH = os.path.abspath(os.getcwd())

    def MakeFile(self):
        if " " in self.text2BeSpoken:
            self.text2BeSpoken = self.text2BeSpoken.replace(" ", " ")
        else:
            self.text2BeSpoken = self.text2BeSpoken
        voice = requests.get(
            f"https://api.carterapi.com/v0/speak/{self.API_KEY}/{self.text2BeSpoken}", stream=True)
        with open(f"{self.PATH}\\temp.mp3", "wb") as f:
            for chunk in voice.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    def Speak(self):
        self.MakeFile()
        mixer.init()
        mixer.music.load(f"{self.PATH}\\temp.mp3")
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(1)
        mixer.quit()

