#!/usr/bin/env python3

from requests import get
from bs4 import BeautifulSoup
from re import findall, DOTALL


def scrapingPage(url, tag, type, value, expresion):
    page = get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return list(map(lambda x: findall(expresion, str(x), DOTALL)[0], soup.findAll(tag, {type: value})))

def obtenerEnlaceCapitulo(urlOnePiece, urlCapitulo):
    headers = {'referer': urlOnePiece}
    page = get(urlCapitulo, headers=headers, allow_redirects=False)
    return page.headers['Location'].replace('paginated', 'cascade')


# for i in scrapingPage('https://tmofans.com/library/manga/45/one-piece', 'li', 'class', 'list-group-item p-0 bg-light', 'Capítulo (\d+.?\d+):? *(.*?)? *</a>.*?<a.*?href="(https?://tmofans.com/goto/\d+)".*?>'):
#     print(i)

# page = get(urlCapitulo)
# urlImages = findall('<img.*?class="viewer-image".*?src="(.*?)".*?/>', page.text, DOTALL)

# page = scrapingPage('https://tmofans.com/viewer/5c0a296dc7830/cascade', 'img', 'class', 'viewer-image', 'src="(.*?)"')
# print(page)