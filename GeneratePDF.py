#!/usr/bin/env python3
# coding: utf8
__author__ = "Juan Manuel Fernández Nácher"

# Librerías del sistema
from os import remove
from os import path
from os import makedirs

# Librería para generar PDF's
# doc: https://pypi.python.org/pypi/pdfkit
# install: pip install pdfkit
from pdfkit import from_file

from requests import get

class GeneratePDF:

	def __init__(self):
		None

	def generatePDF_FromUrlImages(self, pathBase, name, urls):
		directorio = '{0}/{1}'.format(pathBase, name)
		if not path.exists(directorio):
			makedirs(directorio)
		
		for url in urls:
			self.__downloadImage__(directorio, url)
		
		directoriosImagenes = self.__getDirectoriosFromUrls__(directorio, urls)
		return self.__generatePDF_FromImages__(directorio, name, directoriosImagenes)
    
	def __generatePDF_FromImages__(self, directorio, name, directoriosImagenes):
		try:
			outFilename = "{0}.pdf".format(directorio)
			if not path.isfile(outFilename):
				sourceHTML = '<!DOCTYPE html><html><body>'
				for image in directoriosImagenes:
					sourceHTML += '<img src="{0}" width="100%" />'.format(image)
				sourceHTML += '</body></html>'
				
				htmlFile = "{0}.html".format(name)
				htmlFileHandler = open(htmlFile, "w")
				htmlFileHandler.write(sourceHTML)
				htmlFileHandler.close()
				
				from_file(htmlFile, outFilename)
				remove(htmlFile)
			
			return outFilename
		except Exception as ex:
			error = "Error in generatePDF: {0}".format(str(ex))
			print(error)
			return None
	
	def __downloadImage__(self, directorio, url):
		rutaFile = self.__getRutaFileFromUrl__(directorio, url)
		if not path.isfile(rutaFile):
			image = get(url)
			if image.ok:
				with open(rutaFile, "wb") as f:
					f.write(image.content)
	
	def __getDirectoriosFromUrls__(self, directorio, urls):
		return list(map(lambda url: self.__getRutaFileFromUrl__(directorio, url), urls))
	
	def __getRutaFileFromUrl__(self, directorio, url):
		return '{0}/{1}'.format(directorio, url.split('/')[-1])

"""
g = GeneratePDF()
g.generatePDF_FromUrlImages('OnePiece', '927', ['https://img1.tmofans.com/uploads/5c0a296dc7830/e9cb744b.jpg', 'https://img1.tmofans.com/uploads/5c0a296dc7830/6527f09a.jpg'])
"""
