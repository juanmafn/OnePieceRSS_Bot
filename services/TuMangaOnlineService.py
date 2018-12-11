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

from utils.GeneratePDF import GeneratePDF


import sys
sys.path.append('../')


class TuMangaOnlineService:

    def __init__(self):
        self.CAPITULOS = {}
        self.CAPITULO = {}
        self.urlOnePiece = 'https://tmofans.com/library/manga/45/one-piece'

    def obtenerListadoCapitulos(self, userId):
        expresion = 'Capítulo (\d+.?\d+):? *(.*?)? *</a>.*?<a.*?href="(https?://tmofans.com/goto/\d+)".*?>'
        self.CAPITULOS[userId] = scrapingPage(self.urlOnePiece, 'li', 'class', 'list-group-item p-0 bg-light', expresion)
        return self.CAPITULOS[userId]

    def obtenerCapitulo(self, userId, capitulo):
        self.CAPITULO[userId] = capitulo
        capitulo[2] = obtenerEnlaceCapitulo(self.urlOnePiece, capitulo[2])
        capitulo[1] = capitulo[1].strip()
        return capitulo

    def obtenerUltimoCapitulo(self, userId):
        capitulos = self.obtenerListadoCapitulos(userId)
        return self.obtenerCapitulo(userId, list(capitulos[0]))
    
    def descargarCapituloPDF(self, userId):
        capitulo = self.CAPITULO[userId]
        urlImages = scrapingPage(capitulo[2], 'img', 'class', 'viewer-image', 'src="(.*?)"')
        g = GeneratePDF()
        capitulo.append(g.generatePDF_FromUrlImages('OnePiece', capitulo[0], urlImages))
        return capitulo
