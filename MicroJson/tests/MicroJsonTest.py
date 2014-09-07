#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projekt : cosa
  
       File : MicroJsonTest
      Datum : 13.07.14
      Autor : rkruggel
  Copyright : Roland Kruggel, 2014
  
  Bescheibung:
   ...
"""
import time
import unittest
import os
import shutil

from MicroJson import MicroJson

__author__ = 'rkruggel'


class MicroJsonTest(unittest.TestCase):
    DICT_PATH = '../.testdb'
    DICT_FILE = 't_dict.json'
    DICT_FULLPATH = DICT_PATH + '/' + DICT_FILE
    DICT_LISTFILE = 't_list.json'
    DICT_LISTFULLPATH = DICT_PATH + '/' + DICT_LISTFILE

    def inst_dict(self, para=True):
        """Instanz erzeugen"""
        tb = MicroJson(self.DICT_FULLPATH, para)
        self.assertIsInstance(tb, MicroJson, msg="MicroJson (Dict) kann nicht instanziert werden")
        return MicroJson(self.DICT_FULLPATH, para)

    def inst_list(self, para=True):
        """Instanz erzeugen"""
        tl = MicroJson(self.DICT_LISTFULLPATH, para)
        self.assertIsInstance(tl, MicroJson, msg="MicroJson (List) kann nicht instanziert werden")
        return MicroJson(self.DICT_LISTFULLPATH, para)

    def setUp(self):
        """"""
        self.tb = self.inst_dict()
        self.tl = self.inst_list()
        self.dt = time.time()
        self.dt100 = int(self.dt / 100)

    def tearDown(self):
        """"""
        pass

    def test000(self):
        """ Der erste Test ist eigentlich kein test. Er löscht die DB. In
        diesem Fall das gesamte subdir
        """
        try:
            shutil.rmtree(self.DICT_PATH)
        except:
            pass

    def test001_dict_makeinstanze(self):
        """ init dict
        Eine ganz neue Instanz erzeugen """
        self.tb = self.inst_dict(False)
        self.assertTrue(os.path.exists(self.DICT_FULLPATH),
                        msg="MicroJson (dict) kann nicht instanziert werden. File nicht da")

    def test001_list_makeinstanze(self):
        """ init list
        Eine ganz neue Instanz erzeugen """
        self.tb = self.inst_list(False)
        self.assertTrue(os.path.exists(self.DICT_LISTFULLPATH),
                        msg="MicroJson (list) kann nicht instanziert werden. File nicht da")


    def test002_dict_makeinstanze(self):
        """ init dict
        Eine Instanz erzeugen wenn sie schon da ist """
        self.tb = self.inst_dict(True)
        self.assertTrue(os.path.exists(self.DICT_FULLPATH),
                        msg="MicroJson (dict) kann nicht zum zweiten mal instanziert werden. File nicht da")

    def test002_list_makeinstanze(self):
        """ init list
        Eine Instanz erzeugen wenn sie schon da ist """
        self.tb = self.inst_list(True)
        self.assertTrue(os.path.exists(self.DICT_LISTFULLPATH),
                        msg="MicroJson (list) kann nicht zum zweiten mal instanziert werden. File nicht da")

    #
    # diverse 1
    #

    def test010_dict_id(self):
        """ diverses
        Id holen
        """
        # dt = int(time.time() / 100)
        id = self.tb.getId()
        b = int(float(id) / 100)
        self.assertTrue(b == self.dt100)

    def test010_list_id(self):
        """ diverses
        Id holen
        """
        # dt = int(time.time() / 100)
        id = self.tl.getId()
        b = int(float(id) / 100)
        self.assertTrue(b == self.dt100)

    def test011_dict_count(self):
        """ diverses
        Anzahl der vorhandenen Datensätze
        """
        dd = self.tb.count()
        self.assertTrue(dd == 0)

    def test011_list_count(self):
        """ diverses
        Anzahl der vorhandenen Datensätze
        """
        dd = self.tl.count()
        self.assertTrue(dd == 0)

    def test012_dict_exist(self):
        """ diverses
        Sind Datensätze vorhanden
        """
        dd = self.tb.exist()
        self.assertFalse(dd)

    def test012_list_exist(self):
        """ diverses
        Sind Datensätze vorhanden
        """
        dd = self.tl.exist()
        self.assertFalse(dd)


    #
    # insert
    #

    # -01a-
    def test020_dict_insert(self):
        """ insert
        Insert im dict """
        data = {'name': 'petra', 'alter': 54, 'id': '4710'}
        self.id2 = self.tb.set(data)
        assert '4710' == self.id2

    # -01b-
    def test020_list_insert(self):
        """ insert
        Insert in list """
        data = {'tell': 'gewitter', 'tale': 'Es blitzt und donnert'}
        nid = self.tl.setlist(data, xdictid='101', xlistid='20')
        self.assertTrue(nid == '20')


    # -02a-
    def test021_dict_insert(self):
        """ insert
        Insert im dict """
        data = {'name': 'roland', 'alter': 54}
        self.id1 = self.tb.set(data)
        assert str(self.dt100) in self.id1

    def test021_list_insert(self):
        """ insert
        Insert im dict """
        data = {'tell': 'sturm', 'tale': 'Es windet seer'}
        nid = self.tl.setlist(data, xlistid='20')
        self.assertTrue(nid == '20')


    # -03a-
    def test022_dict_insert(self):
        """ insert
        Insert im dict """
        data = {'name': 'roland', 'alter': 54, 'id': '4711'}
        self.id2 = self.tb.set(data)
        assert '4711' == self.id2

    def test022_list_insert(self):
        """ insert
        Insert im dict """
        data = {'tell': 'regen', 'tale': 'it\'s raining cats and dogs'}
        nid = self.tl.setlist(data, xlistid='20')
        self.assertTrue(nid == '20')


    # -04a-
    def test024_dict_insert(self):
        """ insert
        Insert im dict """
        data = {'name': 'roland', 'alter': 54, 'id': '4711'}
        self.id3 = self.tb.set(data, '4711b')
        assert '4711b' == self.id3

    def test024_list_insert(self):
        """ insert
        Insert im dict """
        data = {'tell': 'schnee', 'tale': 'weisser pflaum liegt auf dem zaunpfosten'}
        nid = self.tl.setlist(data, xlistid='20')
        self.assertTrue(nid == '20')


    #
    # diverse 2
    #

    # todo: hier gehts weiter
    def test030_count(self):
        """ diverses
        Anzahl der vorhandenen Datensätze
        """
        dd = self.tb.count()
        self.assertTrue(dd > 0)

    def test031_exist(self):
        """ diverses
        Sind Datensätze vorhanden
        """
        dd = self.tb.exist()
        self.assertTrue(dd)

    #
    # get
    #

    def test040_get01(self):
        """ get
        Ein vorhandener Datensatz """
        dd = self.tb.get('4711')
        self.assertIsNotNone(dd)
        assert dd['name'] == 'roland'
        assert dd['alter'] == 54
        assert dd['id'] == '4711'

    def test041_get02(self):
        """ get
        Einen nicht vorhandener Datensatz
        :return:
        """
        dd = self.tb.get('515151515151515')
        self.assertIsNone(dd)

    def test044_change(self):
        """ change
        daten ändern und wieder lesen """
        dd = self.tb.get('4711')
        self.assertIsNotNone(dd)

        dd['alter'] = 60
        nic = self.tb.set(dd, '4711')
        self.assertTrue(nic == '4711')

    def test045_get03(self):
        """ get
        Ein vorhandener Datensatz """
        dd = self.tb.get('4711')
        self.assertIsNotNone(dd)
        assert dd['name'] == 'roland'
        assert dd['alter'] == 60
        assert dd['id'] == '4711'

    def test050_remove(self):
        """ delete
        datensatz löschen """
        nic = self.tb.rem('4711b')
        self.assertTrue(nic)
        dd = self.tb.get('4711b')
        self.assertIsNone(dd)
        a = 0


    #
    # ende
    #

    def test999(self):
        """
        Aufräumen
        """
        pass


if __name__ == '__main__':
    unittest.main(verbosity=10)

