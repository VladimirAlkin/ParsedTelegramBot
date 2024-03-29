import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

class stop_game:
    host = 'https://stopgame.ru'
    url = 'https://stopgame.ru/review/new'
    lastkey = ""
    lastkey_file = ""

    def __init__(self, lastkey_file):
        self.lastkey_file = lastkey_file

        if os.path.exists(lastkey_file):
            self.lastkey = open(lastkey_file, 'r').read()
        else:
            f = open(lastkey_file, 'w')
            self.lastkey = self.get_lastkey()
            f.write(self.lastkey)
            f.close()

    def new_games(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        new = []
        items = html.select('.tiles > .items > .item > a')
        for i in items:
            key = self.parse_href(i['href'])
            if (self.lastkey < key):
                new.append(i['href'])
        return new

    def game_info(self, uri):
        link = self.host + uri
        r = requests.get(link)
        html = BS(r.content, 'html.parser')

        # parse poster image url
        poster = re.match(r'background-image:\s*url\((.+?)\)', html.select('.image-game-logo > .image')[0]['style'])

        # remove some stuff
        remels = html.select('.article.article-show > *')
        for remel in remels:
            remel.extract()

        # form data
        info = {
            "id": self.parse_href(uri),
            "title": html.select('.article-title > a')[0].text,
            "link": link,
            "image": poster.group(1),
            "score": self.identify_score(html.select('.game-stopgame-score > .score')[0]['class'][1]),
            "excerpt": html.select('.article.article-show')[0].text[0:200] + '...'
        }

        return info

    def download_image(self, url):
        r = requests.get(url, allow_redirects=True)

        a = urlparse(url)
        filename = os.path.basename(a.path)
        open(filename, 'wb').write(r.content)

        return filename

    def identify_score(self, score):
        if (score == 'score-1'):
            return "Мусор 👎"
        elif (score == 'score-2'):
            return "Проходняк ✋"
        elif (score == 'score-3'):
            return "Похвально 👍"
        elif (score == 'score-4'):
            return "Изумительно 👌"



    def get_lastkey(self):
        r = requests.get(self.url)
        html = BS(r.content, "html.parser")
        items = html.select('.titles > .items > .item > a')
        return self.parse_href(items[0]['href'])

    def parse_href(self, href):
        result = re.match(r'\/show\/(\d+)', href)
        return result.group()

    def update_lastkey(self, new_key):
        self.lastkey = new_key

        with open(self.lastkey_file, 'r+') as f:
            data = f.read()
            f.seek(0)
            f.write(str(new_key))
            f.truncate()

        return new_key
