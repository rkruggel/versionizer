#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projekt : versionizer

       File : versionizer
      Datum : 02.07.14
      Autor : rkruggel
  Copyright : Roland Kruggel, 2014

  Bescheibung:
   ...
"""
import os
import datetime
import time
import argparse
import json

__author__ = 'rkruggel'

gCwd = None

parser = argparse.ArgumentParser(description='Incrementiert die Versionen und dokumentiert das kompilieren.')


class pStatics(object):
    @staticmethod
    def getVersionfile():
        return result.cwd + '/' + result.version_file

    @staticmethod
    def getHistoryfile():
        return result.cwd + '/' + result.history_file


class PBasic(object):
    ccFile = ''  # filename der Json-Datei
    ccJson = {}  # Inhalt der Json-Datei

    ccFormat = '%d.%m.%Y %H:%M:%S'  # generelles Format der Datum/Zeit Angabe

    def __init__(self):
        self.jetzt = time.strftime(self.ccFormat, time.localtime())

    a = 0

    def _read(self):
        try:
            with open(self.ccFile, 'r') as infile:
                self.ccJson = json.load(infile)
        except:
            pass


    def _write(self):
        try:
            with open(self.ccFile, 'w') as outfile:
                json.dump(self.ccJson, outfile, indent=4)
        except:
            pass


class PVersion(PBasic):
    """
        version.json bearbeiten
    """

    def __init__(self):
        PBasic.__init__(self)
        self.ccFile = pStatics.getVersionfile()
        self._read()

    def init(self):
        if self.ccFile:
            self.ccJson = {'date': self.jetzt, 'version': '0.0.1', 'build': 0}
            self._write()

    def increment_build(self):
        self.ccJson['build'] = str(int(self.ccJson['build']) + 1)
        self.ccJson['date'] = self.jetzt
        self._write()


class PCompile(PBasic):
    """
        history.json bearbeiten
    """

    def __init__(self):
        PBasic.__init__(self)
        self.ccFile = pStatics.getHistoryfile()
        self._read()

    def init(self):
        if self.ccFile:
            self.ccJson = [{'start': self.jetzt, 'end': self.jetzt, 'minutes': 0}]
            self._write()

    def makezeit(self, lastline, linenr):
        """
        Die letzte Zeit berechnen bevor die neue Zeile eingefügt wird.
        :param lastline:
        :param linenr:
        :return:
        """
        t1 = datetime.datetime.strptime(lastline['start'], self.ccFormat)
        t2 = datetime.datetime.strptime(lastline['end'], self.ccFormat)
        diff = t2 - t1
        self.ccJson[linenr]['minutes'] = int(diff.total_seconds() / 60)

    def insertnewline(self):
        """
        Eine neue Zeile einfügen
        :return:
        """
        js = {'start': self.jetzt, 'end': self.jetzt, 'minutes': 0}
        self.ccJson.append(js)

    def increment_history(self):
        llnr = len(self.ccJson) - 1  # last Line Nr -1

        # wenn daten gelesen wurden
        if llnr >= 0:
            lastline = self.ccJson[llnr]

            # datum/zeit von jetzt
            # aktuelle datum/Zeit (datetime)
            nun1 = datetime.datetime.now()


            # endzeit holen und umrechen (datetime)
            nun2 = datetime.datetime.strptime(lastline['end'], self.ccFormat)

            # differenz
            difftime = nun1 - nun2
            diff30 = (difftime - datetime.timedelta(minutes=30)).total_seconds()

            if diff30 > 0:
                # Differenz ist größer 30 minuten. Neue Zeile einfügen.
                self.makezeit(lastline, llnr)
                self.insertnewline()
                self._write()
            else:
                # Differenz ist kleiner als 30 Minuten. Der Wert 'end' wird aktualisiert
                self.ccJson[llnr]['end'] = self.jetzt
                self.makezeit(lastline, llnr)
                self._write()


# -------------------------------------------------------------------------

parser.add_argument('-i', '--init',
                    action='store_true',
                    default=False,
                    help='Erstellt die files version.json und history.json')
parser.add_argument('-fv',
                    action='store', dest='version_file',
                    default='version.json',
                    help='Name des Version-File ohne Pfad (default: version.json)')
parser.add_argument('-fh',
                    action='store', dest='history_file',
                    default='history.json',
                    help='Name des History-File ohne Pfad (default: history.json)')
parser.add_argument('-wd',
                    action='store', dest='cwd',
                    default=os.getcwd(),
                    help='Das working direktory')
parser.add_argument('-q', '--quit',
                    action='store_true', dest='quit', default=False,
                    help='keine ausgabe auf der console')

result = parser.parse_args()


def printconsole(key, value):
    if not result.quit:
        print key + ': ' + value


if __name__ == "__main__":

    a = 0

    if result.init:
        # gVersionFilename = result.version_file
        o1 = PVersion()
        o1.init()

        # gHistoryFilename = result.history_file
        o2 = PCompile()
        o2.init()
        exit()

    if len(result.version_file) > 0:
        # gVersionFilename = result.version_file
        _dd = pStatics.getVersionfile()
        o1 = PVersion()
        if not os.path.exists(pStatics.getVersionfile()):
            o1.init()
        o1.increment_build()

    if len(result.history_file) > 0:
        # gHistoryFilename = result.history_file
        o2 = PCompile()
        if not os.path.exists(pStatics.getHistoryfile()):
            o2.init()
        o2.increment_history()

    print 'ja' if result.quit else 'nein'

    gCwd = result.cwd

    # Usage example.
    printconsole('working path', gCwd)
    printconsole('version file path', pStatics.getVersionfile())
    printconsole('history file path', pStatics.getHistoryfile())
