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
import os
import datetime
import time
import argparse
import json
import pprint

from microjason.src.jsonpickle import JsonDictDb


# from jsonpickle import JsonListDb


JSONDB_PREFIX = 'jsondb_'
JSONDB_PATH = 'jsondb'

gCwd = None
gConfig = {}

version_dict = {}
version_list = []

version_data = {
    "date": "01.01.1970 00:00:00",
    "major": 0,
    "minor": 0,
    "revision": 0,
    "build": 0
}

class PStatics(object):
    """ Statische Klasse.
    """

    @staticmethod
    def getVersionfile():
        return result.cwd + '/' + 'version.json'

    @staticmethod
    def getDbVersionfile():
        return result.cwd + '/' + JSONDB_PATH + '/' + JSONDB_PREFIX + 'version.json'

    @staticmethod
    def getHistoryfile():
        return result.cwd + '/' + 'history.json'

    @staticmethod
    def getDbHistoryfile():
        return result.cwd + '/' + JSONDB_PATH + '/' + JSONDB_PREFIX + 'history.json'

    @staticmethod
    def printconsole(key, value):
        if not result.quit:
            print key + ': ' + str(value)


class PBasic(object):
    ccFile = ''  # filename der Json-Datei
    ccJson = {}  # Inhalt der Json-Datei

    ccFormat = '%d.%m.%Y %H:%M:%S'  # generelles Format der Datum/Zeit Angabe
    data = {}
    ddb = None

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
            PStatics.printconsole('Version', self.ccJson)
        except:
            pass


class PVersion(PBasic):
    """
        version.json bearbeiten
    """

    def __init__(self):
        PBasic.__init__(self)
        self.init()

    def init(self):
        # self.ccFile = PStatics.getVersionfile()
        self.ddb = JsonDictDb(PStatics.getDbVersionfile(), False)
        self.data = self.ddb.get('1')
        if not self.ddb.exist():
            db = {
                'date': self.jetzt,  # time.localtime(),
                'major': 0,
                'minor': 0,
                'revision': 1,
                'build': 0,
            }
            self.ddb.set('1', db)
            self.ddb.save()

    def write_versionfile(self):
        self.data = self.ddb.get('1')
        pprint.pprint(
            {
                'date': self.data['date'],
                'version': str(self.data['major']) + '.' + str(self.data['minor']) + '.' + str(self.data['revision']),
                'build': self.data['build']
            }
        )

        self._write()

    def increment_build(self):
        # self.data = self.ddb.get('1')
        self.data['build'] += 1
        self.data['date'] = self.jetzt
        self.ddb.save()

    def increment_major(self):
        self.data['major'] += 1
        self.data['minor'] = 0
        self.data['revision'] = 0
        self.ddb.save()

    def increment_minor(self):
        self.data['minor'] += 1
        self.data['revision'] = 0
        self.ddb.save()

    def increment_revision(self):
        self.data['revision'] += 1
        self.ddb.save()


class PHistory(PBasic):
    """
        history.json bearbeiten
    """

    def __init__(self):
        PBasic.__init__(self)
        self.init()

    def init(self):
        self.ddb = JsonDictDb(PStatics.getDbHistoryfile(), False)

        a = 0

        if not self.ddb.exist():
            db = {
                'start': self.jetzt,
                'end': self.jetzt,
                'minutes': 0,
            }
            nic = self.ddb.setlist(db, xlistid='1')
            self.ddb.save()

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
        """
        Die letzte Zeit berechnen bevor die neue Zeile eingefügt wird.
        :param lastline:
        :param linenr:
        :return:
        """
        t1 = datetime.datetime.strptime(lastline['start'], self.ccFormat)
        t2 = datetime.datetime.strptime(lastline['end'], self.ccFormat)
        diff = t2 - t1
        return int(diff.total_seconds() / 60)

    def insertnewline(self):
        """
        Eine neue Zeile einfügen
        :return:
        """
        js = {'start': self.jetzt, 'end': self.jetzt, 'minutes': 0}
        return js

    def increment_history(self):
        a = 0
        lastIds = self.ddb.getall()
        coo = self.ddb.count()
        # lastIds.sort(reverse=True)

        # lastId = lastIds[0]

        t1 = self.ddb.get('1')
        t2 = self.ddb.getlist('1', 0)

        t0 = self.ddb.getlast()

        self.data = self.ddb.getlistlast('1')

        a = 0

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

            # im vorhandenen Datensatz die Zeit setzen
            self.data['minutes'] = self.makezeit(self.data)
            # einen neuen Datensatz einfügen
            # self.ddb.set(self.ddb.getId(), self.insertnewline())
            self.ddb.setlist(self.data, xdictid='1')
        else:
            # Differenz ist kleiner als 30 Minuten. Der Wert 'end' wird aktualisiert
            self.data['end'] = self.jetzt
            self.data['minutes'] = self.makezeit(self.data)

        self.ddb.save()

    def listen(self):
        """ listet die History files auf und stellt sie zum Ändern bereit """

        pprint.pprint(self.ddb.db)


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
parser.add_argument('-li', '--list', action='store_true', dest='listen', default=False,
                    help='Die Version printen')

result = parser.parse_args()


def run():
    gCwd = result.cwd

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
        # gHistoryFilename = result.history_file
        ph = PHistory()

        if result.insert:
            ph.increment_history()

        # print 'ja' if result.quit else 'nein'

        # Usage example.
        # PStatics.printconsole('working path', gCwd)
        # PStatics.printconsole('version file path', PStatics.getVersionfile())
        # PStatics.printconsole('history file path', PStatics.getHistoryfile())


if __name__ == "__main__":
    run()


