import SpeechSynthesis
import BigQueryV2
import SpeechRecognition
import nltk
import time
import requests


class Jarvis:
    def __init__(self):
        self.SpeechSynthesis = SpeechSynthesis.SpeechSynthesis
        self.BigQuery = BigQueryV2.BigQueryV2
        self.SpeechRecognition = SpeechRecognition.SpeechRecognition

    def Speak(self, text):
        self.SpeechSynthesis(text).Speak()
    
    def ListenAndTranscribe(self):
        return self.SpeechRecognition().ListenAndTranscribe()
    
    def BigQuery(self, query):
        return self.BigQuery(query).Query()
    
    def Time(self):
        currTime = time.strftime("%H:%M:%S")
        currTime = currTime.replace(":", " ")
        currTime = currTime.split(" ")
        return currTime

    def Greating(self):
        currTime = self.Time()
        if currTime[0] < 12:
            timePeriod = "morning"
        elif currTime[0] < 18:
            timePeriod = "afternoon"
        else:
            timePeriod = "evening"
          




def apiRes(userRequest):
    API_KEY = "0sww17AF6iXk8lbmRtx25dYWceuY6kf1"
    r = requests.post('https://api.carterapi.com/v0/chat', json={
        'api_key': '0sww17AF6iXk8lbmRtx25dYWceuY6kf1',
        'query': f'{userRequest}',
        'uuid': "user-id-123",
    })


    agent_response = r.json()
    print(agent_response['output']['text'])



apiRes("hello")