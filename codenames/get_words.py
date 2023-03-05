import sys
from typing import List
import random

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

#options = webdriver.ChromeOptions()
#options.add_argument('--ignore-certificate-errors')
#options.add_argument('--incognito')
#options.add_argument('--headless')
#
#driver = webdriver.Chrome(chrome_options=options)
##source =driver.get('https://analyticsindiamag.com/')
#source =driver.get("https://relatedwords.org/relatedto/secretion")
#source_code=driver.page_source
#
#soup = BeautifulSoup(source_code,'html')
#article_block =soup.find('div',class_='words')



def build_options() -> webdriver.chrome.options.Options:
    """
        Factory to make webdriver options
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    return options


def build_driver(options: webdriver.chrome.options.Options) -> webdriver.chrome.webdriver.WebDriver: 
    """
        Factory to build chrome web driver
    """
    driver = webdriver.Chrome(chrome_options=options)
    return driver


class RelatedWordsClient:

    def __init__(self, driver: webdriver.chrome.webdriver.WebDriver):
        self._driver: webdriver.chrome.webdriver.WebDriver = driver 

    def make_url(self, word: str) -> str:
        """
            Create url to find related words, URL escaping the word
        """
        word = word.replace(" ", "%20").lower()
        url = f"https://relatedwords.org/relatedto/{word}"
        return url

    def get_page_source(self, url: str) -> str:
        """
            Load a page and return the page source as a string
        """
        self._driver.get(url)
        page_source = self._driver.page_source
        return page_source

    def get_related_words(self, word: str) -> List[str]:
        print(f"Processing {word}")
        url = self.make_url(word=word)
        source_code = self.get_page_source(url=url)
        soup = BeautifulSoup(source_code, 'html.parser')
        article_block = soup.find('div',class_='words')
        words = article_block.find_all('a')
        return [word.get_text().strip() for word in words]



class CommonWordFinder:

    def __init__(self, related_words_client: RelatedWordsClient):
        self._related_words_client = related_words_client

    
    def find_common_words(self, team_words: List[str], enemy_words: List[str], neutral_words: List[str]):
    
        team_words = [w.lower() for w in team_words]
        enemy_words = [w.lower() for w in enemy_words]
        neutral_words = [w.lower() for w in neutral_words]

        result_dict = {}
        for team_word in team_words:
            related_words = self._related_words_client.get_related_words(word=team_word)
            for related_word in related_words:
                result_dict.setdefault(related_word, {"good": [], "bad": [], "neutral": []})
                result_dict[related_word]["good"].append(team_word)

        for enemy_word in enemy_words:
            related_words = self._related_words_client.get_related_words(word=enemy_word)
            for related_word in related_words:
                result_dict.setdefault(related_word, {"good": [], "bad": [], "neutral": []})
                result_dict[related_word]["bad"].append(enemy_word)


        for neutral_word in neutral_words:
            related_words = self._related_words_client.get_related_words(word=neutral_word)
            for related_word in related_words:
                result_dict.setdefault(related_word, {"good": [], "bad": [], "neutral": []})
                result_dict[related_word]["neutral"].append(enemy_word)


        for k, v in result_dict.items():
            if len(v["good"]) > 1:
                print(f"{k}: {v}")
                if len(v["bad"]) > 0:
                    print("NOPE!")


all_words = []
with open("worlist.txt", "r", encoding="utf-8") as handle:
    for line in handle:
        all_words.append(line.lower().strip())

random.shuffle(all_words)
    
team_a = all_words[0:9]
team_b = all_words[9:17]
neutral = all_words[17:25]

print(team_a)
print(team_b)
print(neutral)

options = build_options()
driver = build_driver(options=options)
client = RelatedWordsClient(driver=driver)

finder = CommonWordFinder(related_words_client=client)

finder.find_common_words(team_words=team_a, enemy_words=team_b, neutral_words=neutral)

