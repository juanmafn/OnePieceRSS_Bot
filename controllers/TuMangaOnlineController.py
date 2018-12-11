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
        self.service = TuMangaOnlineService()

    ##################
    #### COMANDOS ####
    ##################
    def start(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text='Bienvenido!! Escribe /get para obtener el manga que quieras!')

    def help(self, bot, update):
        chat = update.message.chat
        update.message.reply_text('Escribe /get para obtener el manga que quieras!')

    def get(self, bot, update):
        self.__menuInicial(bot, update)

    #########################
    #### GESTIÓN BOTONES ####
    #########################

    def buttonsController(self, bot, update):
        query = update.callback_query
        chatId = query.message.chat_id
        messageId = query.message.message_id
        userId = None
        if query.message.chat.type == 'private':
            userId = query.message.chat.id
        else:
            userId = query.message.reply_to_message.from_user.id
        data = loads(query.data)
        if data[Comando.User.value] == userId:
            if data[Comando.Accion.value] == Opcion.UltimoCapitulo.value:
                self.__obtenerEnlaceUltimoCapitulo(bot, update, userId, chatId, messageId)
            if data[Comando.Accion.value] == Opcion.Capitulo.value:
                self.service.obtenerListadoCapitulos(userId)
            if data[Comando.Accion.value] == Opcion.PDF.value:
                self.__descargarCapituloPDF(bot, update, userId, chatId, messageId)

    ################
    #### LÓGICA ####
    ################

    def __menuInicial(self, bot, update):
        userId = update.message.from_user.id

        layout = [
            [
                {
                    'label': 'Último capítulo',
                    'callback': dumps({Comando.Accion.value: Opcion.UltimoCapitulo.value, Comando.User.value: userId})
                }
            ],
            [
                {
                    'label': 'Capítulo concreto',
                    'callback': dumps({Comando.Accion.value: Opcion.Capitulo.value, Comando.User.value: userId})
                }
            ]
        ]

        update.message.reply_text('¿Qué quieres obtener?', reply_markup=createInlineKeyboardMarkup(layout))


    def __obtenerEnlaceUltimoCapitulo(self, bot, update, userId, chatId, messageId):
        capitulo = self.service.obtenerUltimoCapitulo(userId)
        text = 'Capítulo {0}\n{1}\n{2}'.format(capitulo[0], capitulo[1], capitulo[2])
        print(text)
        layout = [
            [
                {
                    'label': 'Descargar PDF',
                    'callback': dumps({Comando.Accion.value: Opcion.PDF.value, Comando.User.value: userId})
                }
            ]
        ]
        bot.editMessageText(text=text, chat_id=chatId, message_id=messageId, reply_markup=createInlineKeyboardMarkup(layout))
    

    def __descargarCapituloPDF(self, bot, update, userId, chatId, messageId):
        bot.editMessageText(text='Descargando capítulo...', chat_id=chatId, message_id=messageId)
        capitulo = self.service.descargarCapituloPDF(userId)
        pdf = open(capitulo[3], 'rb')
        text = 'Capítulo {0}\n{1}\n{2}'.format(capitulo[0], capitulo[1], capitulo[2])
        bot.sendDocument(chat_id=userId, document=pdf, caption=text)
        if userId == chatId: # canal privado
            bot.deleteMessage(chat_id=chatId, message_id=messageId)
        else: # es un grupo
            bot.editMessageText(text=text, chat_id=chatId, message_id=messageId)
        capitulo.close()
