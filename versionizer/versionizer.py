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

parser = argparse.ArgumentParser(description='Incrementiert die Versionen und dokumentiert das kompilieren.')


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

    def __init__(self, version_file):
        PBasic.__init__(self)
        self.ccFile = version_file
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
        compile.json bearbeiten
    """

    def __init__(self, compile_file):
        PBasic.__init__(self)
        self.ccFile = compile_file
        self._read()

    def init(self):
        if self.ccFile:
            self.ccJson = [{'start': self.jetzt, 'end': self.jetzt, 'zeit': 0}]
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
        self.ccJson[linenr]['zeit'] = int(diff.total_seconds() / 60)

    def insertnewline(self):
        """
        Eine neue Zeile einfügen
        :return:
        """
        js = {'start': self.jetzt, 'end': self.jetzt, 'zeit': 0}
        self.ccJson.append(js)

    def increment_compile(self):
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
                self._write()


parser.add_argument('-i', '--init', action='store_true', default=False,
                    help='Erstellt die files version.json und compile.json')
parser.add_argument('-fv', action='store', dest='version_file', default='',
                    help='Name des Versionierungs File')
parser.add_argument('-fc', action='store', dest='compile_file', default='',
                    help='Name des Compile File')

result = parser.parse_args()

if result.init:
    o1 = PVersion(result.version_file)
    o1.init()

    o2 = PCompile(result.compile_file)
    o2.init()
    exit()

if len(result.version_file) > 0:
    o1 = PVersion(result.version_file)
    if not os.path.exists(result.version_file):
        o1.init()
    o1.increment_build()

if len(result.compile_file) > 0:
    o2 = PCompile(result.compile_file)
    if not os.path.exists(result.compile_file):
        o2.init()
    o2.increment_compile()



