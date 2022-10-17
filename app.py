import SpeechSynthesis
import BigQueryV2
import SpeechRecognition
import nltk
import time
import requests
from random import randint
from requests_html import HTMLSession
import socket




class Jarvis:
    def __init__(self):
        self.SpeechSynthesis = SpeechSynthesis.SpeechSynthesis
        self.BigQuery = BigQueryV2.BigQueryV2
        self.SpeechRecognition = SpeechRecognition.SpeechRecognition

    def ConnectionCheck(self):
        try:
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            pass
        return False

    def Speak(self, text):
        self.SpeechSynthesis(text).Speak()
    
    def ListenAndTranscribe(self):
        return self.SpeechRecognition().ListenAndTranscribe()
    
    def BigQuery(self, query):
        return self.BigQuery(query).Search()
    
    def Time(self):
        currTime = time.strftime("%H:%M:%S")
        currTime = currTime.replace(":", " ")
        currTime = currTime.split(" ")
        return currTime

    def WeatherInformation(self,rawInput):
        from requests_html import HTMLSession
        from nltk import tokenize
        s = HTMLSession()
        pos = 0
        place = tokenize.word_tokenize(rawInput)
        if "keyword" in place:
            for x in range(int(len(place))):
                if place[x] == "keyword":
                    pos = x+1
            place = rawInput[pos:]
            url = f'https://www.google.com/search?q=what+is+the+weather+in+{place}'
        else:
            place = "my current location"
            url = f'https://www.google.com/search?q=what+is+the+weather+at+{place}'
        r = s.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.75'})
        temp = r.html.find('span#wob_tm', first=True).text
        unit = r.html.find('div.vk_bk.wob-unit span.wob_t', first=True).text
        desc = r.html.find('div.VQF4g', first=True).find(
            'span#wob_dc', first=True).text
        place = r.html.find('div.wob_loc', first=True).text
        res = f"It is {temp}{unit} and it's {desc} in {place}"
        return res

    def Greating(self):
        weatherRep = self.WeatherInformation(" ")
        currTime = self.Time()
        if currTime[0] < 12:
            timePeriod = "morning"
        elif currTime[0] < 18:
            timePeriod = "afternoon"
        else:
            timePeriod = "evening"
        ranNum = randint(0, 4)
        statements = [f"Good {timePeriod}",f"Good {timePeriod}, the time is {timePeriod}",f"Good {timePeriod}, {weatherRep}"]
        return statements[ranNum]

    def apiRes(self,command):
        API_KEY = "0sww17AF6iXk8lbmRtx25dYWceuY6kf1"
        r = requests.post('https://api.carterapi.com/v0/chat', json={
            'api_key': '0sww17AF6iXk8lbmRtx25dYWceuY6kf1',
            'query': f'{command}',
            'uuid': "user-id-123",
        })


        agent_response = r.json()
        return agent_response

    def checkCustomTriggers(self,api_response):
        customTriggers = api_response["triggers"]
        numOfActivatedTriggers = 0
        for trigger in customTriggers:
            numOfActivatedTriggers += 1
        arrayOfCustomTriggers = [str() for x in range(numOfActivatedTriggers)]
        loopCounter = 0
        for trigger in customTriggers:
            arrayOfCustomTriggers[loopCounter] = trigger['type']
            loopCounter += 1

        return arrayOfCustomTriggers

    def main(self):
        connection = self.ConnectionCheck()
        micActivation = input(str("Please select a mic activation method (Certain keystroke)"))
        micActivation = ord(f"{micActivation}")
        activationCheck = ""
        while connection:
            activation = False
            while not activation:
                activationCheck = ord(input(str("Enter activation key:")))
                if activationCheck == micActivation:
                    activation = True
            command = self.ListenAndTranscribe()
            apiRes = self.apiRes(command)
            triggers = self.checkCustomTriggers(apiRes)
            for trigger in triggers:
                if trigger == "Big-Query":
                    response = self.BigQuery(command)
                if trigger == "Weather-Information":
                    response = self.WeatherInformation(command)
                if trigger == "Time":
                    response = self.Time()
            
            self.Speak(response)
                    