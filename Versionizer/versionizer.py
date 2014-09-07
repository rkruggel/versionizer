#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projekt : cosa

       File : cosa
      Datum : 02.07.14
      Autor : rkruggel
  Copyright : Roland Kruggel, 2014

  Bescheibung:
   ...
"""
from StdSuites.Text_Suite import paragraph

import sys
# sys.path.append('/Users/rkruggel/Dropbox/Develop/Python/cosa/exe')

import os
import datetime
import time
import argparse
import json
import pprint

import os
import time
# from datetime import datetime


from MicroJson import JsonDictDb

# from exe.MicroJsonBasic.MicroJsonBasic import *


JSONDB_PREFIX = 'jsondb_'
JSONDB_PATH = 'jsondb'

gPath = None

gCwd = None
gConfig = {}

version_dict = {}
version_list = []

version_data = {
    "id": "1",
    "date": "01.01.1970 00:00:00",
    "major": 0,
    "minor": 0,
    "revision": 0,
    "build": 0
}

history_data = {
    "id": "1",
    "start": "01.01.1970 00:00:00",
    "end": "01.01.1970 00:00:00",
    "minutes": 0
}

a = 0


class PStatics(object):
    """ Statische Klasse.
    """

    VERSION_FILE = 'version.json'
    HISTORY_FILE = 'history.json'

    @staticmethod
    def getVersionfile():
        global gPath
        #return result.cwd + '/' + PStatics.VERSION_FILE
        if gPath is None:
            st = result.cwd
        else:
            st = result.cwd + '/' + gPath
        aa = os.path.exists(st)
        a=0

    @staticmethod
    def getDbVersionfile():
        return result.cwd + '/' + JSONDB_PATH + '/' + JSONDB_PREFIX + PStatics.VERSION_FILE

    @staticmethod
    def getHistoryfile():
        return result.cwd + '/' + PStatics.HISTORY_FILE

    @staticmethod
    def getDbHistoryfile():
        return result.cwd + '/' + JSONDB_PATH + '/' + JSONDB_PREFIX + PStatics.HISTORY_FILE

    @staticmethod
    def printconsole(key, value):
        if not result.quit:
            print key + ': ' + str(value)


class PBasic(object):
    ccFile = ''  # filename der Json-Datei
    ccJson = {}  # Inhalt der Json-Datei

    ccFormat = '%d.%m.%Y %H:%M:%S'  # generelles Format der Datum/Zeit Angabe
    micodb = None

    def __init__(self):
        self.jetzt = time.strftime(self.ccFormat, time.localtime())

    def getNewId(self):
        return str(int(round(time.time() * 1000)))

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
            PStatics.printconsole('Version', self.ccJson)
        except:
            pass


class PVersion(PBasic):
    """
        version.json bearbeiten
    """
    micodb = None

    def __init__(self):
        PBasic.__init__(self)
        self.init()

    def init(self):
        self.micodb = JsonDictDb(PStatics.getVersionfile(), False)

        if not self.micodb.exist():
            self.micodb.set(version_data)
            self.micodb.save()

    def write_versionfile(self):
        da = self.micodb.get('1')
        pprint.pprint(
            {
                'date': da['date'],
                'version': str(da['major']) + '.' + str(da['minor']) + '.' + str(da['revision']),
                'build': da['build']
            }
        )
        self._write()

    def save_version(self):
        self.micodb.save()

    def increment_build(self):
        da = self.micodb.get('1')
        da['build'] += 1
        da['date'] = self.jetzt
        self.save_version()

    def increment_major(self):
        da = self.micodb.get('1')
        da['major'] += 1
        da['minor'] = '0'
        da['revision'] = '0'
        self.save_version()

    def increment_minor(self):
        da = self.micodb.get('1')
        da['minor'] += 1
        da['revision'] = 0
        self.save_version()

    def increment_revision(self):
        da = self.micodb.get('1')
        da['revision'] += 1
        self.save_version()


class PHistory(PBasic):
    """
        history.json bearbeiten
    """

    data = None

    def __init__(self):
        PBasic.__init__(self)
        self.init()

    def init(self):
        self.micodb = JsonDictDb(PStatics.getHistoryfile(), False)

        if not self.micodb.exist():
            # self.micodb.set(history_data)
            # self.micodb.save()

            # da = self.micodb.get("1")
            self.micodb.set(self.getNewDataset())
            self.micodb.save()

    def getNewDataset(self, da=None):
        if da is None:
            da = history_data
        da['id'] = self.getNewId()
        da['start'] = self.jetzt
        da['end'] = self.jetzt
        return da

    # (IMHO) the simplest approach:
    def sortedDictValues1(adict):
        items = adict.items()
        items.sort()
        return [value for key, value in items]

    # an alternative implementation, which
    # happens to run a bit faster for large
    # dictionaries on my machine:
    def sortedDictValues2(adict):
        keys = adict.keys()
        keys.sort()
        return [dict[key] for key in keys]

    # a further slight speed-up on my box
    # is to map a bound-method:
    def sortedDictValues3(adict):
        keys = adict.keys()
        keys.sort()
        return map(adict.get, keys)

    def makezeit(self, lastline):
        """ Die letzte Zeit berechnen bevor die neue Zeile eingefügt wird.
        :param lastline:
        :return:
        """
        t1 = datetime.datetime.strptime(lastline['start'], self.ccFormat)
        t2 = datetime.datetime.strptime(lastline['end'], self.ccFormat)
        diff = t2 - t1
        return int(diff.total_seconds() / 60)

    def increment_history(self):
        a = 0

        self.data = self.micodb.getlast()

        # self.data = self.micodb.getlistlast('1')
        # self.data = []

        newid = self.getNewId()

        a = self.micodb.getId()

        # datum/zeit von jetzt
        # aktuelle datum/Zeit (datetime)
        nun1 = datetime.datetime.now()

        # endzeit holen und umrechen (datetime)
        nun2 = datetime.datetime.strptime(self.data['end'], self.ccFormat)

        # differenz
        difftime = nun1 - nun2
        diff30 = (difftime - datetime.timedelta(minutes=30)).total_seconds()

        if diff30 > 0:
            # Differenz ist größer 30 minuten. Neue Zeile einfügen.

            # im vorhandenen Datensatz die anzahl der Minuten setzen
            self.data['minutes'] = self.makezeit(self.data)
            # einen neuen Datensatz einfügen
            self.micodb.set(self.getNewDataset())
        else:
            # Differenz ist kleiner als 30 Minuten. Der Wert 'end' wird aktualisiert
            self.data['end'] = self.jetzt
            self.data['minutes'] = self.makezeit(self.data)

        self.micodb.save()

    def listen(self):
        """ listet die History files auf """
        pprint.pprint(self.micodb.db)


# -------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Incrementiert die Versionen und dokumentiert das kompilieren.')

# -- diverses
parser.add_argument('-wd',
                    action='store', dest='cwd',
                    default=os.getcwd(),
                    help='Das working direktory')
parser.add_argument('-q', '--quit',
                    action='store_true', dest='quit', default=False,
                    help='Keine Ausgabe auf der console')

parser.add_argument('--path', action='store', dest='setpath',
                    help='Der Pfad in dem die Datenfiles abgelegt werden.')

# -- version
parser.add_argument('--version', action='store_true', dest='version', default=False,
                    help='Jeder befehl der Version wird hiermit eingeleitet.')
parser.add_argument('-vb', '--build', action='store_true', dest='build', default=False,
                    help='Erhöht die Build Nr.')
parser.add_argument('-va', '--major', action='store_true', dest='major', default=False,
                    help='Die Major-Nr wird um eins erhöht')
parser.add_argument('-vi', '--minor', action='store_true', dest='minor', default=False,
                    help='Die Minor-Nr wird um eins erhöht')
parser.add_argument('-vr', '--rev', action='store_true', dest='revision', default=False,
                    help='Die Revisions-Nr wird um eins erhöht')

parser.add_argument('-vp', '--vprint', action='store_true', dest='vprint', default=False,
                    help='Die Version printen')

# -- history
parser.add_argument('--history', action='store_true', dest='history', default=False,
                    help='Jeder Befehl der History wird hiermit eingeleitet.')
parser.add_argument('-hi', '--insert', action='store_true', dest='insert', default=False,
                    help='Fügt einen Datensatz in die History ein')
parser.add_argument('-li', '--list', action='store_true', dest='list', default=False,
                    help='Die Version printen')

result = parser.parse_args()


def run():
    global gPath
    global gCwd

    gCwd = result.cwd

    if result.setpath:
        gPath = result.setpath

    if result.version:
        pv = PVersion()

        if result.build:
            pv.increment_build()

        if result.major:
            pv.increment_major()

        if result.minor:
            pv.increment_minor()

        if result.revision:
            pv.increment_revision()

        if result.vprint:
            pv.write_versionfile()

    if result.history:
        ph = PHistory()

        if result.insert:
            ph.increment_history()

        if result.list:
            ph.listen()


if __name__ == "__main__":
    run()


