#!/usr/bin/env python3

from enum import Enum


class Comando(Enum):
    Accion = 'a'
    Opcion = 'o'
    User = 'u'
    

class Opcion(Enum):
    Ultimo = '1'
    Capitulo = '2'
    PDF = '3'
    CANCEL = '4'
    USER = '5'
    BEGIN = '<<'
    LEFT = '<'
    ACTUAL = '.'
    RIGHT = '>'
    END = '>>'
