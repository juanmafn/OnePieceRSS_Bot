#!/usr/bin/env python3

from controllers.TuMangaOnlineController import TuMangaOnlineController


def config():
    controller = TuMangaOnlineController()
    return {
        'commands': [
            {
                'command': 'start',
                'function': controller.start
            },
            {
                'command': 'help',
                'function': controller.help
            },
            {
                'command': 'get',
                'function': controller.get
            }
        ],
        'buttons': controller.buttonsController,
        'nocommand': None
    }
