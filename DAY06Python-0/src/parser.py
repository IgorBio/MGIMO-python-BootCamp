import json
import random
from bs4 import BeautifulSoup


class Parser:

    def __init__(self, source):
        self.__source = source

    def parser(self):
        with open(self.__source, "r", encoding='utf-8') as f:
            html = f.read()
        html = BeautifulSoup(html, "lxml")
        fact = random.choice(html.find_all(class_='p-2 clearfix'))
        self.__information = list(fact.text)
        return self.__information

    def save(self, file_path):
        with open(file_path, "w") as outfile:
            outfile.write(json.dumps(self.__information))



