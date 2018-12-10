#!/usr/bin/env python3

# Librería bot telegram
# doc: https://github.com/python-telegram-bot/python-telegram-bot
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from models.Enumeradores import Opcion
from models.Enumeradores import Comando
from services.TuMangaOnlineService import TuMangaOnlineService
from api.Botones import createInlineKeyboardMarkup
from json import loads, dumps
import sys
sys.path.append('../')


class TuMangaOnlineController:
    def __init__(self):
        self.CAPITULOS = {}
        self.urlOnePiece = 'https://tmofans.com/library/manga/45/one-piece'

    ##################
    #### COMANDOS ####
    ##################
    def start(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text='Bienvenido!! Escribe /get para obtener el manga que quieras!')

    def help(self, bot, update):
        chat = update.message.chat
        update.message.reply_text('Escribe /get para obtener el manga que quieras!')

    def get(self, bot, update):
        userId = update.message.from_user.id

        layout = [
            [
                {
                    'label': 'Último capítulo',
                    'callback': dumps({Comando.Accion.value: Opcion.Ultimo.value, Comando.User.value: userId})
                }
            ], [
                {
                    'label': 'Capítulo concreto',
                    'callback': dumps({Comando.Accion.value: Opcion.Capitulo.value, Comando.User.value: userId})
                }
            ]
        ]

        update.message.reply_text('¿Qué quieres obtener?', reply_markup = createInlineKeyboardMarkup(layout))

    #########################
    #### GESTIÓN BOTONES ####
    #########################

    def buttonsController(self, bot, update):
        None

    ################
    #### LÓGICA ####
    ################
    def prueba(self):
        a = TuMangaOnlineService()
        a.prueba()
