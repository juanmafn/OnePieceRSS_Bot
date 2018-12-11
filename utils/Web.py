#!/usr/bin/env python3

from requests import get
from bs4 import BeautifulSoup
from re import findall, DOTALL


def scrapingPage(url, tag, type, value, expresion):
    page = get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    #print(str(soup.findAll(tag, {type: value})[0]))
    return list(map(lambda x: findall(expresion, str(x), DOTALL), soup.findAll(tag, {type: value})))

def obtenerEnlaceCapitulo(urlOnePiece, urlCapitulo):
    headers = {'referer': urlOnePiece}
    print(headers)
    print(urlCapitulo)
    page = get(urlCapitulo, headers=headers, allow_redirects=False)
    print(page.headers['Location'])
    return page.headers['Location'].replace('paginated', 'cascade')


# for i in scrapingPage('https://tmofans.com/library/manga/45/one-piece', 'li', 'class', 'list-group-item p-0 bg-light', 'Capítulo (\d+.?\d+):? *(.*?)? *</a>.*?<a.*?href="(https?://tmofans.com/goto/\d+)".*?>'):
#     print(i)