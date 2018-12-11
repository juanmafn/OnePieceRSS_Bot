#!/usr/bin/env python3

# Librería bot telegram
# doc: https://github.com/python-telegram-bot/python-telegram-bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from requests import get
from bs4 import BeautifulSoup
from re import findall, DOTALL
from json import loads, dumps

from utils.Web import scrapingPage
from utils.Web import obtenerEnlaceCapitulo

import sys
sys.path.append('../')


class TuMangaOnlineService:

    def __init__(self):
        self.CAPITULOS = {}
        self.urlOnePiece = 'https://tmofans.com/library/manga/45/one-piece'

    def obtenerListadoCapitulos(self, userId):
        tag = 'li'
        type = 'class'
        value = 'list-group-item p-0 bg-light'
        expresion = 'Capítulo (\d+.?\d+):? *(.*?)? *</a>.*?<a.*?href="(https?://tmofans.com/goto/\d+)".*?>'
        self.CAPITULOS[userId] = scrapingPage(self.urlOnePiece, tag, type, value, expresion)
        return self.CAPITULOS[userId]

    def obtenerUltimoCapitulo(self, userId):
        capitulos = self.obtenerListadoCapitulos(userId)
        capitulo = list(capitulos[0][0])
        capitulo[2] = obtenerEnlaceCapitulo(self.urlOnePiece, capitulo[2])
        capitulo[1] = capitulo[1].strip()
        return capitulo
