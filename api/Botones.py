#!/usr/bin/env python3
# coding: utf8
__author__ = "Juan Manuel Fernández Nácher"

# Librería bot telegram
# doc: https://github.com/python-telegram-bot/python-telegram-bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def createInlineKeyboardMarkup(layout):
    keyboard = []
    for row in layout:
        keyboard_row = []
        for col in row:
            keyboard_row.append(InlineKeyboardButton(col['label'], callback_data=col['callback']))
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(keyboard)
