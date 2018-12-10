#!/usr/bin/env python3
# coding: utf8
__author__ = "Juan Manuel Fernández Nácher"

# Librería bot telegram
# doc: https://github.com/python-telegram-bot/python-telegram-bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters

import sys
sys.path.append('../')


class TelegramApi:
    def __init__(self, token, config):
        self.token = token
        self.config = config

    def startBot(self):
        # Create the Updater and pass it your bot's token.
        updater = Updater(self.token)

        # Listenings - comands
        if self.config['commands'] != None:
            for command in self.config['commands']:
                updater.dispatcher.add_handler(CommandHandler(command['command'], command['function']))

        # Buttons controller
        if self.config['buttons'] != None:
            updater.dispatcher.add_handler(CallbackQueryHandler(self.config['buttons']))

        # Listening noncamnd
        if self.config['nocommand'] != None:
            updater.dispatcher.add_handler(MessageHandler(Filters.text, self.config['nocommand']))

        # log all error
        updater.dispatcher.add_error_handler(self.__error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT
        updater.idle()

    def __error(self, bot, update, error):
        None
