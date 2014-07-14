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

from MicroJson import JsonDictDb
import MicroJson

__author__ = 'rkruggel'

import unittest
import os
import shutil


class MicroJsonTest(unittest.TestCase):
    DICT_FILE = 't_dict.json'
    DICT_PATH = '../.testdb'
    DICT_FULLPATH = DICT_PATH + '/' + DICT_FILE


    # def __init__(self):
    # super(MicroJsonTest, self).__init__()
    # fi = '../.testdb'
    #     try:
    #         shutil.rmtree(fi)
    #     except:
    #         pass

    def inst(self, para=True):
        """Instanz erzeugen"""
        tb = MicroJson.JsonDictDb(self.DICT_FULLPATH, para)
        self.assertIsInstance(tb, MicroJson.JsonDictDb, msg="JsonDictDb kann nicht instanziert werden")
        return MicroJson.JsonDictDb(self.DICT_FULLPATH, para)

    def setUp(self):
        """"""
        self.tb = self.inst()
        self.dt = time.time()
        self.dt2 = int(self.dt / 100)

    def tearDown(self):
        """"""
        pass

    def test000(self):
        """ Der erste Test ist eigentlich kein test. Er löscht die DB
        """
        try:
            shutil.rmtree(self.DICT_PATH)
        except:
            pass

    def test001_make_instanze(self):
        """ init
        Eine ganz neue Instanz erzeugen """
        self.tb = self.inst(False)
        self.assertTrue(os.path.exists(self.DICT_FULLPATH),
                        msg="JsonDictDb kann nicht instanziert werden. File nicht da")

    def test001_make_instanze2(self):
        """ init
        Eine Instanz erzeugen wenn sie schon da ist """
        self.tb = self.inst(True)
        self.assertTrue(os.path.exists(self.DICT_FULLPATH),
                        msg="JsonDictDb kann nicht zum zweiten mal instanziert werden. File nicht da")

    #
    # diverse 1
    #

    def test004_id(self):
        """ diverses
        Id holen
        """
        # dt = int(time.time() / 100)
        id = self.tb.getId()
        b = int(float(id) / 100)
        self.assertTrue(b == self.dt2)

    def test010_count(self):
        """ diverses
        Anzahl der vorhandenen Datensätze
        """
        dd = self.tb.count()
        self.assertTrue(dd == 0)

    def test011_exist(self):
        """ diverses
        Sind Datensätze vorhanden
        """
        dd = self.tb.exist()
        self.assertFalse(dd)


    #
    # insert
    #

    def test020_insertdict00(self):
        """ insert
        Insert im dict """
        data = {'name': 'petra', 'alter': 54, 'id': '4710'}
        self.id2 = self.tb.set(data)
        assert '4710' == self.id2

    def test021_insertdict01(self):
        """ insert
        Insert im dict """
        data = {'name': 'roland', 'alter': 54}
        self.id1 = self.tb.set(data)
        assert str(self.dt2) in self.id1

    def test022_insertdict02(self):
        """ insert
        Insert im dict """
        data = {'name': 'roland', 'alter': 54, 'id': '4711'}
        self.id2 = self.tb.set(data)
        assert '4711' == self.id2

    def test024_insertdict03(self):
        """ insert
        Insert im dict """
        data = {'name': 'roland', 'alter': 54, 'id': '4711'}
        self.id3 = self.tb.set(data, '4711b')
        assert '4711b' == self.id3

    #
    # diverse 2
    #

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
        a=0


    #
    # ende
    #

    def test999(self):
        """
        Aufräumen
        """
        fi = '../.testdb'
        # shutil.rmtree(fi)
        # self.assertFalse(os.path.exists(fi), msg="Dir kann nicht gelöscht werden")


if __name__ == '__main__':
    unittest.main(verbosity=10)

