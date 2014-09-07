#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projekt : cosa

       File : cosa
      Datum : 02.07.14
      Autor : rkruggel
  Copyright : Roland Kruggel, 2014

  Bescheibung:
    Micro Json
    Es können Daten schemafrei in form einer Key-Value nosql gespeichert werden.

  Anleitung:

"""
import os
import time
import json


JSONDB_PREFIX = 'jsondb_'
JSONDB_PATH = 'jsondb'


class pickleDb(object):
    loco = None  # der filename
    fsave = None  # True -> es soll gespeichert werden
    db = {}  # die DB als dict

    def __init__(self, location, option):
        """Creates a database object and loads the data from the location path.
        If the file does not exist it will be created on the first update."""
        self.load(location, option)

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

    def dump(self):
        """Force save memory db to file."""
        self._dumpdb(True)
        return True

    def set(self, key, value):
        """Set the (string,int,whatever) value of a key"""
        self.db[key] = value
        self._dumpdb(self.fsave)
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
        self._dumpdb(self.fsave)
        return True

    def lcreate(self, name):
        """Create a list"""
        self.db[name] = []
        self._dumpdb(self.fsave)
        return True

    def ladd(self, name, value):
        """Add a value to a list"""
        self.db[name].append(value)
        self._dumpdb(self.fsave)
        return True

    def lgetall(self, name):
        """Return all values in a list"""
        return self.db[name]

    def lget(self, name, pos):
        """Return one value in a list"""
        return self.db[name][pos]

    def lrem(self, name):
        """Remove a list and all of its values"""
        number = len(self.db[name])
        del self.db[name]
        self._dumpdb(self.fsave)
        return number

    def lpop(self, name, pos):
        """Remove one value in a list"""
        value = self.db[name][pos]
        del self.db[name][pos]
        self._dumpdb(self.fsave)
        return value

    def llen(self, name):
        """Returns the length of the list"""
        return len(self.db[name])

    def append(self, key, more):
        """Add more to a key's value"""
        tmp = self.db[key]
        self.db[key] = ('%s%s' % (tmp, more))
        self._dumpdb(self.fsave)
        return True

    def lappend(self, name, pos, more):
        """Add more to a value in a list"""
        tmp = self.db[name][pos]
        self.db[name][pos] = ('%s%s' % (tmp, more))
        self._dumpdb(self.fsave)
        return True

    def dcreate(self, name):
        """Create a dict"""
        self.db[name] = {}
        self._dumpdb(self.fsave)
        return True

    def dadd(self, name, pair):
        """Add a key-value pair to a dict, "pair" is a tuple"""
        self.db[name][pair[0]] = pair[1]
        self._dumpdb(self.fsave)
        return True

    def dget(self, name, key):
        """Return the value for a key in a dict"""
        return self.db[name][key]

    def dgetall(self, name):
        """Return all key-value pairs from a dict"""
        return self.db[name]

    def drem(self, name):
        """Remove a dict and all of its pairs"""
        del self.db[name]
        self._dumpdb(self.fsave)
        return True

    def dpop(self, name, key):
        """Remove one key-value in a dict"""
        value = self.db[name][key]
        del self.db[name][key]
        self._dumpdb(self.fsave)
        return value

    def dkeys(self, name):
        """Return all the keys for a dict"""
        return self.db[name].keys()

    def dvals(self, name):
        """Return all the values for a dict"""
        return self.db[name].values()

    def dexists(self, name, key):
        """Determine if a key exists or not"""
        if self.db[name][key] is not None:
            return 1
        else:
            return 0

    def deldb(self):
        """Delete everything from the database"""
        self.db = {}
        self._dumpdb(self.fsave)
        return True

    def _loaddb(self):
        """Load or reload the json info from the file"""
        # self.db = simplejson.load(open(self.loco, 'rb'))
        self.db = json.load(open(self.loco, 'rb'))

    def _dumpdb(self, forced):
        """Dump (write, save) the json dump into the file"""
        if forced:
            # simplejson.dump(self.db, open(self.loco, 'wb'))
            json.dump(self.db, open(self.loco, 'wb'))


class MicroJsonBasic(object):
    path = None  # nur der dirname
    file = None  # nur der filename
    loco = None  # der full filename
    fsave = None  # True -> es soll gespeichert werden
    db = {}  # die DB als dict

    def __init__(self, location, option):
        location = os.path.expanduser(location)
        self.path = os.path.dirname(location)
        self.file = os.path.basename(location)
        self.loco = self.path + '/' + self.file
        self.fsave = option

        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def _loaddb(self):
        """ Load or reload the json info from the file
        :return:
        """
        self.db = json.load(open(self.loco, 'rb'))

    def _savedb(self, forced):
        """ Dump (write, save) the json save into the file
        :param forced:
        :return:
        """
        if forced:
            json.dump(self.db, open(self.loco, 'wb'), indent=4)

    #
    # diverses
    #

    def getId(self):
        return "%.6i" % time.time()


class MicroJson(MicroJsonBasic):
    def __init__(self, location, option):
        """ Creates a database object and loads the data from the location path.
            If the file does not exist it will be created on the first update.

        >>> fi = '../.testdb/t_dict.json'
        >>> tb = MicroJson(fi, False)
        >>> os.path.exists(fi)
        True
        >>> import shutil
        >>> fi = '../.testdb/'
        >>> shutil.rmtree(fi)
        """
        super(MicroJson, self).__init__(location, option)
        self.db = {}
        if not os.path.exists(self.loco):
            self._savedb(True)
        self.load()

    #
    # laden / speichern
    #

    def load(self):
        """ Loads, reloads or changes the path to the db file.
            DO NOT USE this method has it may be deprecated in the future.
        """
        # if os.path.exists(location):
        self._loaddb()
        # else:
        # self.db = {}
        return True

    def save(self):
        """ Force save memory db to file.
        """
        ss = self.db
        self._savedb(True)
        return True

    #
    # set/get
    #

    # ## -------------------------------------------------------------------------------------
    def set(self, value, xid=None):
        """
            :param value: zu speichernder wert. Es handelt sich hierbei immer
                        um ein dict.
            :return:
        """
        a = 0

        if not isinstance(value, dict):
            raise Exception("error: value: muss vom type 'dict' sein.")

        value, _id = self._set_addid(value, xid)

        # -- Datensatz wird gesucht.
        # Datensatz vorhanden -> Datensatz ändern
        # Datensatz nicht vorhanden -> Datensatz hinzufügen
        if self.exist(_id):
            # -- change
            self.db[_id] = value
            self._savedb(self.fsave)
        else:
            # -- insert
            self.db[_id] = value
            self._savedb(self.fsave)

        return _id

    def setlist(self, value, xdictid=None, xlistid=None):

        a = 0

        # -- value muss ein dict sein
        if not isinstance(value, dict):
            raise Exception("error: value: muss vom type 'dict' sein.")

        # -- Id's creieren
        value, _id = self._set_addid(value, xdictid)
        if None == xlistid:
            xlistid = self.getId()

        # -- die vorhandene List holen. Wenn noch keine vorhanden ist
        # wird sie erstellt.
        if not self.exist(xlistid):
            self.db[xlistid] = []

        a = 0

        # if datensatz nicht vorhanden then:
        self.db[xlistid].append(value)
        self._savedb(self.fsave)

        return xlistid

    def _set_addid(self, value, xid=None):
        """ Erzeugt wenn nötig eine ID und fügt diese dem Dict hinzu.

            Das dict 'value' hat immer ein Feld 'Id'. Wenn diese nicht vorhanden ist, wird
            sie in das dict eingefügt.

            Eine Id 'None' ist bedeutet das immer, das eine ID erzeugt wird.

            Wenn der parameter xid <> None ist wird dieser wert als ID genommen

            :param value: Das dict
            :param xid: Die ID, wenn vorhanden
            :return:
        """
        a = 0

        _id = None

        # -- die Id aus value holen
        if value.has_key('id'):
            _id = value['id']

        # -- wenn xid vorhanden, dann ist es gültg
        if not None == xid:
            _id = xid

        if _id == None:
            # -- Wenn die ID 0 oder leer ist, dann wird eine neue
            # automatische ID vergeben.
            _id = self.getId()
            # return self.set(value, _id)

        if not isinstance(_id, (str, unicode)):
            raise Exception('error iujk: value["id"] muss ein string sein')

        value['id'] = _id

        a = 0

        return value, _id


    # ## -------------------------------------------------------------------------------------
    def get(self, xid):
        """ Get the value of a key"""
        try:
            return self.db[xid]
        except KeyError:
            return None

    def getlist(self, xid, xlistid):
        """ Get one item of the list"""
        try:
            return self.get(xid)[xlistid]
        except KeyError:
            return None

    def getkeys(self):
        """ Return a list of all keys in db"""
        return self.db.keys()

    def getall(self):
        return self.db

    def getfirst(self):
        key = self.getkeys()
        key.sort()
        return self.get(key[0])

    def getlast(self):
        key = self.getkeys()
        key.sort(reverse=True)
        return self.get(key[0])

    def getlistlast(self, xid):
        a = 0
        dd = self.get(xid)
        dd.sort(reverse=True)

        data = dd[0]
        return data

    def rem(self, xid):
        """ Delete a key"""
        del self.db[xid]
        self._savedb(self.fsave)
        return True

    def count(self):
        """
            :return: Anzahl der Datensätze in der db
        """
        return len(self.db)

    def exist(self, xid=''):
        """
            :return: True, wenn datensätze existieren
        """
        if xid == '':
            return self.count() >= 1

        ss = self.get(xid)
        if not ss:
            return False

        return True


# class JsonListDb(MicroJsonBasic):
# def __init__(self, location, option):
# """Creates a database object and loads the data from the location path.
# If the file does not exist it will be created on the first update."""
# super(JsonListDb, self).__init__(location, option)
# self.db = []
# if not os.path.exists(self.loco):
# self._savedb(True)
# self.load()
#
#     #
#     # laden / speichern
#     #
#
#     def load(self):
#         """Loads, reloads or changes the path to the db file.
#         DO NOT USE this method has it may be deprecated in the future."""
#         # if os.path.exists(location):
#         self._loaddb()
#         # else:
#         # self.db = []
#         return True
#
#     def save(self):
#         """Force save memory db to file."""
#         self._savedb(True)
#         return True
#
#     #
#     # set/get
#     #
#
#     def set(self, value):
#         """Set the (string,int,whatever) value of a key"""
#         if value['id'] == '0':
#             value['id'] = self.getId()
#             self.db.append(value)
#         # self.db[key] = value
#         # self._savedb(self.fsave)
#         return True
#
#     def get(self, key):
#         """Get the value of a key"""
#         # try:
#         # return self.db[key]
#         # except KeyError:
#         # return None
#         pass
#
#     def getkeys(self):
#         return range(0, len(self.db))
#
#     def getall(self):
#         """Return a list of all keys in db"""
#         return self.db  # .keys()
#
#     def getfirst(self):
#         return self.db[0]
#
#     def getlast(self):
#         return self.db[self.count() - 1]
#
#     def rem(self, key):
#         """Delete a key"""
#         # del self.db[key]
#         # self._savedb(self.fsave)
#         return True
#
#     def count(self):
#         """
#         :return: Anzahl der Datensätze in der db
#         """
#         return len(self.db)
#
#     def exist(self):
#         """
#         :return: True, wenn datensätze existieren
#         """
#         return self.count() >= 1
#

class Illolo:
    def summe(self, a, b):
        """
        addiert zwei zahlen

        >>> kk = Illolo()
        >>> kk.summe(2,4)
        8
        >>> kk = Illolo()
        >>> kk.summe(2)
        Traceback (most recent call last):
            ...
        TypeError: summe() takes exactly 3 arguments (2 given)
        >>> kk = Illolo()
        >>> kk.summe()
        Traceback (most recent call last):
            ...
        TypeError: summe() takes exactly 3 arguments (1 given)
        """

        x = (a + b) + 2
        return x


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    a = 0


    # -------------------------------------------------------------------------
    #
    # -- dict
    #
    # -------------------------------------------------------------------------

    # -- init
    tb = MicroJson('../jsondb/t_dict.json', False)

    # # -- alles lesen
    # datadict = tb.getall()
    #
    # # -- Dict-Datensatz hinzufügen
    # if 0:
    #     datadict = {
    #         'vorname': 'roland',
    #         'name': 'roland',
    #         'alter': 54
    #     }
    #     nid = tb.set(datadict, xid='kl99')
    #
    #     datadict = {
    #         'id': '32',
    #         'vorname': 'petra',
    #         'name': 'kruggel',
    #         'alter': 60
    #     }
    #     tb.set(datadict)
    #
    #     datadict = {
    #         'id': '188',
    #         'vorname': 'Tanja',
    #         'name': 'Othen',
    #         'alter': 26
    #     }
    #     tb.set(datadict, xid='189')
    #
    # # -- Dict-Daten ändern
    # if 0:
    #     # -- den ersten key lesen
    #     keys = tb.getkeys()
    #
    #     # -- den ersten datensatz lesen
    #     datafirst = tb.getfirst()
    #
    #     # -- den letzten datensatz lesen
    #     datalast = tb.getlast()
    #
    #     # -- den ersten datensatz ändern
    #     datafirst['name'] = 'Kruggel.'
    #     datafirst['vorname'] = 'Roland'
    #     tb.set(datafirst)

    # -------------------------------------------------------------------------
    #
    # -- list
    #
    # -------------------------------------------------------------------------

    # -- List-Datensatz hinzufügen
    if 0:
        # liste hinzufügen
        #dd = []
        #nid = tb.set(dd, xid='210')

        # liste füllen
        dd = {
            'tell': 'gewitter',
            'tale': 'Es blitzt und donnert'
        }
        nid = tb.setlist(dd, xdictid='101', xlistid='20')

        dd = {
            'tell': 'sturm',
            'tale': 'Es windet seer'
        }
        nid = tb.setlist(dd, xlistid='20')

    tb.save()


    # if not t_dbb.exist():
    # t_dbb.set(0, {})  # data insert
    # t_dbb.save()

    # -- datensatz schreiben


    a = 0

