from requests_html import HTMLSession
import wikipedia as wiki
import wolframalpha as wolfram
import nltk
import requests


class BigQueryV2:
    def __init__(self, SearchQuery, SearchTerm="keyword"):
        self.session = HTMLSession()
        SearchQuery = nltk.word_tokenize(SearchQuery)
        for x in range(int(len(SearchQuery))):
            if SearchQuery[x] == SearchTerm:
                pos = x+1
                break
        SearchQuery = SearchQuery[pos:]
        SearchQuery = " ".join(SearchQuery)
    def GoogleSearch(self):
        searchQuery = nltk.word_tokenize(self.SearchQuery)
        query = ""
        for x in range(len(searchQuery)):
            query += f'{searchQuery[x]}+'
        query = query[:-1]
        url = f'https://www.google.com/search?q={query}'
        r = self.session.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.75'})
        try:
            scientificInformation = r.html.find('div.kno-rdesc', first=True).text
        except AttributeError:
            scientificInformation = "no scientific information found"
        try:
            generalInformation = r.html.find('span.hgKElc', first=True).text
        except AttributeError:
            generalInformation = "no general information found"
        try:
            scientificFactOne = r.html.find('div.sATSHe', first=True).text
        except AttributeError:
            scientificFactOne = "no scientific fact found"
        try:
            dictionaryDefOne = r.html.find('div.thODed', first=True).text
        except AttributeError:
            dictionaryDefOne = "no definition found"
        try:
            dictionaryDefTwo = r.html.find('div.vmod', first=True).text
        except AttributeError:
            dictionaryDefTwo = "no definition found"
        try:
            fullDescription = r.html.find('div.sATSHe', first=True).text
        except AttributeError:
            fullDescription = "no description found"
        searchRes = [scientificInformation, scientificFactOne, generalInformation, dictionaryDefOne, dictionaryDefTwo, fullDescription]
        for result in searchRes:
            if result == "no scientific information found" or result == "no general information found" or result == "no scientific fact found" or result == "no definition found":
                searchRes = searchRes.remove(result)
        googleSearchResult = ""
        for x in range(len(searchRes)):
            googleSearchResult += f'{searchRes[x]} \n'
        return googleSearchResult
    def WikiSearch(self):
        try:
            ans = wiki.summary(self.SearchQuery, sentences=35)
        except wiki.exceptions.PageError:
            ans = "no wikipedia information found"
        return ans
    def WolframSearch(self):
        app_id = "your app id"
        client = wolfram.Client(app_id)
        try:
            res = client.query(self.SearchQuery)
            ans = next(res.results).text
        except:
            ans = "no wolfram information found"
        return ans
    def TotalAnswer(self):
        googleSearchResult = self.GoogleSearch()
        wikiSearchResult = self.WikiSearch()
        wolframSearchResult = self.WolframSearch()
        totalAnswer = f'{googleSearchResult} \n {wikiSearchResult} \n {wolframSearchResult}'
        return totalAnswer
    def Search(self):
        totalAnswer = self.TotalAnswer()
        API_TOKEN = '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'
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
        output = query({
            "inputs": f"{totalAnswer}", "options": {"use_gpu": True}, "options": {"use_cache": True}, "options": {"wait_for_model": True}, "parameters": {"max_length": 125}
        })
        ans = output[0]['summary_text']
        return ans