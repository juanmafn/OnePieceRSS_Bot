#!/usr/bin/env python3

# Librería bot telegram
# doc: https://github.com/python-telegram-bot/python-telegram-bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from requests import get
from bs4 import BeautifulSoup
from re import findall, DOTALL
from json import loads, dumps

from enum import Enum

from GeneratePDF import GeneratePDF

class Accion(Enum):
	ULTIMO = '1'
	CAPITULO = '2'
	PDF = '3'
	CANCEL = '4'
	USER = '5'
	BEGIN = '<<'
	LEFT = '<'
	ACTUAL = '.'
	RIGHT = '>'
	END = '>>'

class TuMangaOnline:
	
	def __init__(self):
		self.CAPITULOS = {}
	
	def start(self, bot, update):
		userId = update.message.from_user.id
		self.log(bot, update)
		keyboard = []
		callback = dumps({'a': Accion.ULTIMO.value, 'u': userId})
		keyboard.append([InlineKeyboardButton('Último capítulo', callback_data=callback)])
		callback = dumps({'a': Accion.CAPITULO.value, 'u': userId})
		keyboard.append([InlineKeyboardButton('Capítulo concreto', callback_data=callback)])
		reply_markup = InlineKeyboardMarkup(keyboard)
		update.message.reply_text('¿Qué quieres obtener?', reply_markup=reply_markup)
	
	def log(self, bot, update, comentario = None):
		user = None
		messageText = None
		if update.callback_query:
			message = update.callback_query.message
			messageText = message.text
			if message.chat.type == 'private':
				user = message.chat
			else:
				user = message.reply_to_message.from_user
		else:
			user = update.message.from_user
			messageText = update.message.text
		
		text = '@{0} ({1} {2}) @{3} {4}'.format(user.username, user.first_name, user.last_name, bot.username, messageText)
		if comentario != None:
			text += ' ' + comentario
		print(text)
		bot.sendMessage(text=text, chat_id=-364650397)
		
	def buttonController(self, bot, update):
		query = update.callback_query
		chatId = query.message.chat_id
		messageId = query.message.message_id
		userId = None
		if query.message.chat.type == 'private':
			userId = query.message.chat.id
		else:
			userId = query.message.reply_to_message.from_user.id
		data = loads(query.data)
		if data['u'] == userId:
			if data['a'] == Accion.ULTIMO.value:
				if 'o' in data:
					if data['o'] == Accion.PDF.value:
						self.log(bot, update, '<<Descarga PDF>>')
						bot.editMessageText(text='Descargando capítulo...', chat_id=chatId, message_id=messageId)
						self.getUltimoCapitulo(bot, chatId, messageId, userId)
				else:
					self.log(bot, update, '<<Último capítulo>>')
					bot.editMessageText(text='Obteniendo último capítulo', chat_id=chatId, message_id=messageId)
					nCapitulo, urlCapitulo, capitulos = self.__getNombreYUrlUltimoCapitulo()
					keyboard = []
					callback_pdf = dumps({'a': Accion.ULTIMO.value, 'o': Accion.PDF.value, 'u': userId})
					keyboard.append([InlineKeyboardButton('Descargar PDF', callback_data=callback_pdf)])
					reply_markup = InlineKeyboardMarkup(keyboard)
					text = 'Capítulo {0}\nEnlace: {1}'.format(nCapitulo, urlCapitulo)
					bot.editMessageText(text=text, chat_id=chatId, message_id=messageId, reply_markup=reply_markup)
			elif data['a'] == Accion.CAPITULO.value:
				if 'o' in data:
					self.log(bot, update, '<<Pulsado botón({0})>>'.format(data['o']))
					if (
						data['o'] == Accion.BEGIN.value or 
						data['o'] == Accion.LEFT.value or 
						data['o'] == Accion.ACTUAL.value or 
						data['o'] == Accion.RIGHT.value or 
						data['o'] == Accion.END.value
						):
						posicion = int(data['p'])
						nCapitulo = int(data['nc'])
						self.__paginacion__(bot, update, nCapitulo, userId, posicion)
					else:
						if data['o'] == Accion.PDF.value:
							nCapitulo = data['o2']
							bot.editMessageText(text='Descargando capítulo...', chat_id=chatId, message_id=messageId)
							self.getCapitulo(bot, chatId, messageId, nCapitulo, userId)
						else:
							nCapitulo = data['o']
							bot.editMessageText(text='Obteniendo capítulo {0}'.format(nCapitulo), chat_id=chatId, message_id=messageId)
							nCapitulo, urlCapitulo = self.__getNombreYUrlCapitulo(nCapitulo)
							keyboard = []
							callback_pdf = dumps({'a': Accion.CAPITULO.value, 'o': Accion.PDF.value, 'o2': nCapitulo, 'u': userId})
							keyboard.append([InlineKeyboardButton('Descargar PDF', callback_data=callback_pdf)])
							reply_markup = InlineKeyboardMarkup(keyboard)
							text = 'Capítulo {0}\nEnlace: {1}'.format(nCapitulo, urlCapitulo)
							bot.editMessageText(text=text, chat_id=chatId, message_id=messageId, reply_markup=reply_markup)
							#self.getCapitulo(bot, chatId, messageId, nCapitulo)
							#bot.editMessageText(text='Sin implementar', chat_id=chatId, message_id=messageId)
							self.CAPITULOS[userId] = None
				else:
					self.log(bot, update, '<<Obtener un capítulo>>')
					bot.editMessageText(text='Obteniendo listado de capítulos', chat_id=chatId, message_id=messageId)
					nCapitulo, urlCapitulo, capitulos = self.__getNombreYUrlUltimoCapitulo()
					nCapitulo = int(float(nCapitulo))
					self.CAPITULOS[userId] = capitulos
					self.__paginacion__(bot, update, nCapitulo, userId)
			

	def getUltimoCapitulo(self, bot, chatId, messageId, userId):
		directorioPDF, nCapitulo, urlCapitulo = self.__getUltimoCapitulo__()
		self.__sendPDF__(bot, directorioPDF, nCapitulo, urlCapitulo, chatId, messageId, userId)
	
	def getCapitulo(self, bot, chatId, messageId, nCapitulo, userId):
		directorioPDF, nCapitulo, urlCapitulo = self.__getCapitulo__(nCapitulo)
		self.__sendPDF__(bot, directorioPDF, nCapitulo, urlCapitulo, chatId, messageId, userId)
	
	def __sendPDF__(self, bot, directorioPDF, nCapitulo, urlCapitulo, chatId, messageId, userId):
		capitulo = open(directorioPDF, 'rb')
		text = 'Capítulo {0}\nEnlace: {1}'.format(nCapitulo, urlCapitulo)
		bot.editMessageText(text=text, chat_id=chatId, message_id=messageId)
		bot.sendDocument(chat_id=userId, document=capitulo, caption=directorioPDF)
		capitulo.close()
	
	def __getUltimoCapitulo__(self):
		#Obtenemos número del último capítulo y su url
		nCapitulo, urlRedirect, capitulos = self.__getNombreYUrlUltimoCapitulo()
		return self.__downloadCapitulo__(nCapitulo, urlRedirect)
		
	def __getCapitulo__(self, nCapitulo):
		url = 'https://tmofans.com/library/manga/45/one-piece'
		page = get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		s = soup.findAll('li', {'class': 'list-group-item p-0 bg-light'})
		
		for html in s:
			nCap = findall('Capítulo (\d+.?\d{0,5})', str(html), DOTALL)[0]
			if (float(nCap) - int(float(nCap))) == 0:
				nCap = str(int(float(nCap)))
			if nCapitulo == nCap:
				urlCapitulo = findall('<a.*?href="(https?://tmofans.com/goto/\d+)".*?>', str(html), DOTALL)[0]
				headers = {'referer': url}
				page = get(urlCapitulo, headers=headers, allow_redirects=False)
				urlRedirect = page.headers['Location'].replace('paginated', 'cascade')
				return self.__downloadCapitulo__(nCap, urlRedirect)
	
	def __downloadCapitulo__(self, nCapitulo, urlCapitulo):
		# Obtenemos las urls de las imágenes del capítulo
		page = get(urlCapitulo)
		urlImages = findall('<img.*?class="viewer-image".*?src="(.*?)".*?/>', page.text, DOTALL)
		
		# Generamos el PDF del capítulo
		g = GeneratePDF()
		directorio = g.generatePDF_FromUrlImages('OnePiece', nCapitulo, urlImages)
		return directorio, nCapitulo, urlCapitulo
	
	def __getNombreYUrlUltimoCapitulo(self):
		url = 'https://tmofans.com/library/manga/45/one-piece'
		page = get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		s = soup.findAll('li', {'class': 'list-group-item p-0 bg-light'})
		
		capitulos = self.__getNumerosCapitulos__(s)
		
		# Obtenemos el número del capítulo
		nCapitulo = findall('Capítulo (\d+.?\d{0,5})', str(s[0]), DOTALL)[0]
		if (float(nCapitulo) - int(float(nCapitulo))) == 0:
			nCapitulo = str(int(float(nCapitulo)))
		
		# Obtenemos la url del capítulo
		urlCapitulo = findall('<a.*?href="(https?://tmofans.com/goto/\d+)".*?>', str(s[0]), DOTALL)[0]
		headers = {'referer': url}
		page = get(urlCapitulo, headers=headers, allow_redirects=False)
		urlRedirect = page.headers['Location'].replace('paginated', 'cascade')
		
		return nCapitulo, urlRedirect, capitulos
	
	def __getNombreYUrlCapitulo(self, nCapitulo):
		url = 'https://tmofans.com/library/manga/45/one-piece'
		page = get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		s = soup.findAll('li', {'class': 'list-group-item p-0 bg-light'})
		
		for html in s:
			nCap = findall('Capítulo (\d+.?\d{0,5})', str(html), DOTALL)[0]
			if (float(nCap) - int(float(nCap))) == 0:
				nCap = str(int(float(nCap)))
			if nCapitulo == nCap:
				urlCapitulo = findall('<a.*?href="(https?://tmofans.com/goto/\d+)".*?>', str(html), DOTALL)[0]
				headers = {'referer': url}
				page = get(urlCapitulo, headers=headers, allow_redirects=False)
				urlRedirect = page.headers['Location'].replace('paginated', 'cascade')
				
		return nCapitulo, urlRedirect
	
	def __getNumerosCapitulos__(self, s):
		capitulos = []
		for html in s:
			nCapitulo = findall('Capítulo (\d+.?\d{0,5})', str(html), DOTALL)[0]
			if (float(nCapitulo) - int(float(nCapitulo))) == 0:
				nCapitulo = str(int(float(nCapitulo)))
			capitulos.append(nCapitulo)
		return capitulos
	
	def __paginacion__(self, bot, update, nCapitulo, userId, position = 0):
		query = update.callback_query
		chatId = query.message.chat_id
		messageId = query.message.message_id
		text = 'Elige un capítulo'
		
		#opciones = list(range(nCapitulo, 0, -1))
		opciones = self.CAPITULOS[userId]

		keyboard = []
		numCols = 5
		numRows = 8
		block = numCols * numRows
		
		numOpciones = len(opciones)
		parts = int(numOpciones / block)
		if (numOpciones % block) == 0:
			parts -= 1
		
		posInit = 0
		posLeft = position - 1
		if posLeft < 0: posLeft = 0
		posRight = position + 1
		if posRight > parts: posRight = parts
		posEnd = parts
		
		dataInit = dumps({'a': Accion.CAPITULO.value, 'o': Accion.BEGIN.value, 'p': posInit, 'nc': nCapitulo, 'u': userId})
		dataLeft = dumps({'a': Accion.CAPITULO.value, 'o': Accion.LEFT.value, 'p': posLeft, 'nc': nCapitulo, 'u': userId})
		dataActually = dumps({'a': Accion.CAPITULO.value, 'o': Accion.ACTUAL.value, 'p': position, 'nc': nCapitulo, 'u': userId})
		dataRight = dumps({'a': Accion.CAPITULO.value, 'o': Accion.RIGHT.value, 'p': posRight, 'nc': nCapitulo, 'u': userId})
		dataEnd = dumps({'a': Accion.CAPITULO.value, 'o': Accion.END.value, 'p': posEnd, 'nc': nCapitulo, 'u': userId})
		
		keyboard.append([
			InlineKeyboardButton("<< {0}".format(posInit), callback_data=dataInit),
			InlineKeyboardButton("< {0}".format(posLeft), callback_data=dataLeft),
			InlineKeyboardButton("· {0} ·".format(position), callback_data=dataActually),
			InlineKeyboardButton("{0} >".format(posRight), callback_data=dataRight),
			InlineKeyboardButton("{0} >>".format(posEnd), callback_data=dataEnd)])
		
		inicio = position * block
		final = (position + 1) * block
		partOpciones = opciones[inicio:final]
		numPartOpciones = len(partOpciones)
		
		for i in range(0, numPartOpciones, numCols):
			col = numCols
			if (i + col) >= numPartOpciones:
				col = numPartOpciones - i
			keyboard.append([InlineKeyboardButton(str(partOpciones[i+j]), callback_data=dumps({'a': Accion.CAPITULO.value, 'o': str(partOpciones[i+j]), 'u': userId})) for j in range(col)])
		
		reply_markup = InlineKeyboardMarkup(keyboard)
		bot.editMessageText(text=text, chat_id=chatId, message_id=messageId, reply_markup=reply_markup)
		
