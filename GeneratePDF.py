#!/usr/bin/env python3
# coding: utf8
__author__ = "Juan Manuel Fernández Nácher"

# Librerías del sistema
from os import path
from os import makedirs
from os import remove
from shutil import rmtree

# Librería para generar PDF's
# doc: https://pypi.python.org/pypi/pdfkit
# install: pip install pdfkit
from pdfkit import from_file

# Librerías web
from requests import get

# Librerías hilos
from threading import Thread
from threading import Semaphore


class GeneratePDF:

    def __init__(self):
        self.semaforo = Semaphore(10)

    def generatePDF_FromUrlImages(self, pathBase, name, urls):
        directorio = '{0}/{1}'.format(pathBase, name)
        if not path.exists(directorio):
            makedirs(directorio)

        id_hilos = []
        for url in urls:
            idh = Thread(target=self.__downloadImage__, args=(directorio, url))
            idh.start()
            id_hilos.append(idh)
        for idh in id_hilos:
            idh.join()

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
                rmtree(directorio)

            return outFilename
        except Exception as ex:
            error = "Error in generatePDF: {0}".format(str(ex))
            print(error)
            return None

    def __downloadImage__(self, directorio, url):
        self.semaforo.acquire()

        rutaFile = self.__getRutaFileFromUrl__(directorio, url)
        if not path.isfile(rutaFile):
            image = get(url)
            if image.ok:
                with open(rutaFile, "wb") as f:
                    f.write(image.content)
        
        self.semaforo.release()

    def __getDirectoriosFromUrls__(self, directorio, urls):
        return list(map(lambda url: self.__getRutaFileFromUrl__(directorio, url), urls))

    def __getRutaFileFromUrl__(self, directorio, url):
        return '{0}/{1}'.format(directorio, url.split('/')[-1])
