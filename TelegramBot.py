#!/usr/bin/env python3
# coding: utf8
__author__ = "Juan Manuel Fernández Nácher"

# Librería bot telegram
# doc: https://github.com/python-telegram-bot/python-telegram-bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters

from TuMangaOnline import TuMangaOnline

class TelegramBot:
	def __init__(self, token):
		self.token = token
		self.tuMangaOnline = TuMangaOnline()

	def startBot(self):
		# Create the Updater and pass it your bot's token.
		updater = Updater(self.token)

		# Listenings - comands
		updater.dispatcher.add_handler(CommandHandler('start', self.__start))
		updater.dispatcher.add_handler(CommandHandler('help', self.__help))
		updater.dispatcher.add_handler(CommandHandler('get', self.tuMangaOnline.start))

		# Buttons controller
		updater.dispatcher.add_handler(CallbackQueryHandler(self.tuMangaOnline.buttonController))


		# log all error
		updater.dispatcher.add_error_handler(self.__error)

		# Start the Bot
		updater.start_polling()

		# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
		# SIGTERM or SIGABRT
		updater.idle()

	def __start(self, bot, update):
		bot.sendMessage(chat_id=update.message.chat_id, text="Bienvenido!! Escribe /get para obtener el manga que quieras!")

	def __help(self, bot, update):
		chat = update.message.chat
		update.message.reply_text("Escribe /get para obtener el manga que quieras!")

	def __error(self, bot, update, error):
		None
