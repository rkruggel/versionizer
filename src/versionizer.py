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
import simplejson
import string


JSONDB_PREFIX = 'jsondb_'
JSONDB_PATH = 'jsondb'

gCwd = None
gConfig = {}

version_dict = {}
version_list = []


class JsonDb(object):
    loco = None  # der filename
    fsave = None  # True -> es soll gespeichert werden
    db = {}  # die DB als dict

    def __init__(self, location, option):
        """Creates a database object and loads the data from the location path.
        If the file does not exist it will be created on the first update."""
        self.load(location, option)

    #
    # laden / speichern
    #

    def load(self, location, option):
        """Loads, reloads or changes the path to the db file.
        DO NOT USE this method has it may be deprecated in the future."""
        location = os.path.expanduser(location)
        self.loco = location
        self.fsave = option
        if os.path.exists(location):
            self._loaddb()
        else:
            self.db = {}
        return True

    def _loaddb(self):
        """Load or reload the json info from the file"""
        self.db = simplejson.load(open(self.loco, 'rb'))

    def save(self):
        """Force save memory db to file."""
        self._savedb(True)
        return True

    def _savedb(self, forced):
        """Dump (write, save) the json save into the file"""
        if forced:
            simplejson.dump(self.db, open(self.loco, 'wb'))

    #
    # diverses
    #

    # @staticmethod
    def getId(self):
        return time.time()

    #
    # set/get
    #

    def set(self, key, value):
        """Set the (string,int,whatever) value of a key"""
        self.db[key] = value
        self._savedb(self.fsave)
        return True

    def get(self, key):
        """Get the value of a key"""
        try:
            return self.db[key]
        except KeyError:
            return None

    def getall(self):
        """Return a list of all keys in db"""
        return self.db.keys()

    def rem(self, key):
        """Delete a key"""
        del self.db[key]
        self._savedb(self.fsave)
        return True

    def count(self):
        """
        :return: Anzahl der Datensätze in der db
        """
        return len(self.db)

    def exist(self):
        """
        :return: True, wenn datensätze existieren
        """
        return self.count() >= 1


class PDb(JsonDb):
    def __init__(self, location, option):
        JsonDb.__init__(self, location, option)
        if not os.path.exists(JSONDB_PATH):
            os.mkdir(JSONDB_PATH)


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
    def getDbConfigfile():
        return result.cwd + '/' + JSONDB_PATH + '/' + JSONDB_PREFIX + 'config.json'

    @staticmethod
    def printconsole(key, value):
        if not result.quit:
            print key + ': ' + str(value)


class PBasic(object):
    ccFile = ''  # filename der Json-Datei
    ccJson = {}  # Inhalt der Json-Datei

    ccFormat = '%d.%m.%Y %H:%M:%S'  # generelles Format der Datum/Zeit Angabe
    # db = None
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
        self.ccFile = PStatics.getVersionfile()
        self.ddb = PDb(PStatics.getDbVersionfile(), False)
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
        self.ccJson = {'date': self.data['date'],
                       'version': str(self.data['major']) + '.' + str(self.data['minor']) + '.' + str(
                           self.data['revision']),
                       'build': self.data['build']}
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
        self.ddb = PDb(PStatics.getDbHistoryfile(), False)

        if not self.ddb.exist():
            db = {
                'start': self.jetzt,
                'end': self.jetzt,
                'minutes': 0,
            }
            self.ddb.set(self.ddb.getId(), db)
            self.ddb.save()

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
        lastIds = self.ddb.getall()
        lastIds.sort(reverse=True)

        lastId = lastIds[0]
        self.data = self.ddb.get(lastId)

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
            self.ddb.set(self.ddb.getId(), self.insertnewline())
            self.ddb.save()
        else:
            # Differenz ist kleiner als 30 Minuten. Der Wert 'end' wird aktualisiert
            self.data['end'] = self.jetzt
            self.data['minutes'] = self.makezeit(self.data)
            self.ddb.save()


# -------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Incrementiert die Versionen und dokumentiert das kompilieren.')

parser.add_argument('--install', action='store_true', dest='install', default=False,
                    help='Initialisiert die DB und die initfiles')

parser.add_argument('-wd',
                    action='store', dest='cwd',
                    default=os.getcwd(),
                    help='Das working direktory')
parser.add_argument('-q', '--quit',
                    action='store_true', dest='quit', default=False,
                    help='Keine Ausgabe auf der console')

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

parser.add_argument('--history', action='store_true', dest='history', default=False,
                    help='Jeder Befehl der History wird hiermit eingeleitet.')
parser.add_argument('-hi', '--insert', action='store_true', dest='insert', default=False,
                    help='Fügt einen Datensatz in die History ein')

result = parser.parse_args()


def installdb():
    """
    Installiert eine neue db. Muss nur einmal aufgerufen werden.
    :return:
    """
    if not os.path.exists(JSONDB_PATH):
        os.mkdir(JSONDB_PATH)

    # --- config db anlegen/ändern
    inidict = {'name': 'versionizer',
               'mainuser': 'rkruggel',
               'historytime': 46,
               'doVersion': True,
               'doHistory': True,
    }

    db = PDb(PStatics.getDbConfigfile(), False)
    db.set('1', inidict)
    db.save()

    # --- config neu einlesen
    gConfig = getConfig()


def getConfig():
    return PDb(PStatics.getDbConfigfile(), False)


def run():
    gCwd = result.cwd
    conf = PDb(PStatics.getDbConfigfile(), False)
    gConfig = conf.get('1')

    # test
    # if result.vprint:
    # oo = PVersion()
    # oo.write_versionfile()
    # exit()

    if result.install:
        installdb()
        exit()

    # if result.init:
    # o1 = PVersion()
    # o1.init()
    #
    # o2 = PHistory()
    # o2.init()
    # exit()

    # a1 = result.version
    # a2 = gConfig['doVersion']
    if result.version and gConfig['doVersion']:
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

    if result.history and gConfig['doHistory']:
        # gHistoryFilename = result.history_file
        ph = PHistory()

        if result.insert:
            # if not os.path.exists(PStatics.getHistoryfile()):
            # ph.init()
            ph.increment_history()

    print 'ja' if result.quit else 'nein'

    # Usage example.
    PStatics.printconsole('working path', gCwd)
    PStatics.printconsole('version file path', PStatics.getVersionfile())
    PStatics.printconsole('history file path', PStatics.getHistoryfile())


if __name__ == "__main__":
    run()

