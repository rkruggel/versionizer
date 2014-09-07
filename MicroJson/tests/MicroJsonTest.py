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
    # Verzeichniss in dem die Testdb geschrieben wird
    TEST_PATH = '.testdb'
    # Name der TestDb
    TEST_DB = 'test.json'
    TEST_DB_FULLPATH = TEST_PATH + '/' + TEST_DB

    def inst_dict(self, para=True):
        """Instanz erzeugen"""
        tb = MicroJson(self.TEST_DB_FULLPATH, para)
        self.assertIsInstance(tb, MicroJson, msg="MicroJson kann nicht instanziert werden")
        return tb

    def setUp(self):
        """"""
        self.tb = self.inst_dict()
        self.dt = time.time()
        self.dt100 = int(self.dt / 100)

    def tearDown(self):
        """"""
        pass

    #
    # ÄNDERUNGEN
    #


    # inst_dict  -> inst
    # inst_list enfällt

    #
    # TEST BEGIN
    #

    def test_000(self):
        """ Der erste Test ist eigentlich kein test. Er löscht die DB. In
            diesem Fall das gesamte subdir
        """
        try:
            shutil.rmtree(self.TEST_PATH)
        except:
            pass

    def test_201_dict_makeinstanze(self):
        """ init dict
            Eine ganz neue Instanz erzeugen """
        self.tb = self.inst_dict(False)
        self.assertTrue(os.path.exists(self.TEST_DB_FULLPATH),
                        msg="MicroJson kann nicht instanziert werden. File nicht da")

    # obsolete
    # def test_201_list_makeinstanze(self):
    # """ init list
    # Eine ganz neue Instanz erzeugen """
    # self.tb = self.inst_list(False)
    # self.assertTrue(os.path.exists(self.TEST_LISTFULLPATH),
    #                     msg="MicroJson (list) kann nicht instanziert werden. File nicht da")

    def test_202_dict_makeinstanze(self):
        """ init dict
            Eine Instanz erzeugen wenn sie schon da ist """
        self.tb = self.inst_dict(True)
        self.assertTrue(os.path.exists(self.TEST_DB_FULLPATH),
                        msg="MicroJson (dict) kann nicht zum zweiten mal instanziert werden. File nicht da")

    #
    # diverse 1
    #

    def test_210_dict_id(self):
        """ diverses
            Id holen
        """
        # dt = int(time.time() / 100)
        id = self.tb.getId()
        b = int(float(id) / 100)
        self.assertTrue(b == self.dt100)

    def test_211_dict_count(self):
        """ diverses
            Anzahl der vorhandenen Datensätze
        """
        dd = self.tb.count()
        self.assertTrue(dd == 0)

    def test_212_dict_exist(self):
        """ diverses
            Sind Datensätze vorhanden
        """
        dd = self.tb.exist()
        self.assertFalse(dd)

    #
    # set
    #

    # -01a-
    def test_220_set_dict(self):
        """ set
            Insert im dict (mit Id) """
        data = {'name': 'petra', 'alter': 54, 'id': '4710'}
        self.id2 = self.tb.set(data)
        assert '4710' == self.id2

    # -02a-
    def test_221_set_dict(self):
        """ set
        Insert im dict (ohne Id) """
        data = {'name': 'roland', 'alter': 54}
        self.id1 = self.tb.set(data)
        assert str(self.dt100) in self.id1

    # -03a-
    def test_222_set_dict(self):
        """ set
        Insert im dict """
        data = {'name': 'roland', 'alter': 54, 'id': '4711'}
        self.id2 = self.tb.set(data)
        assert '4711' == self.id2

    # -04a-
    def test_224_set_dict(self):
        """ set
        Insert im dict """
        data = {'name': 'roland', 'alter': 54, 'id': '4711'}
        self.id3 = self.tb.set(data, '4711b')
        assert '4711b' == self.id3


    # -01b-
    def test_220_set_list(self):
        """ set
        Insert in list """
        data = {'tell': 'gewitter', 'tale': 'Es blitzt und donnert'}
        nid = self.tb.setlist(data, xdictid='101', xlistid='20')
        self.assertTrue(nid == '20')

    def test_221_set_list(self):
        """ set
        Insert im dict """
        data = {'tell': 'sturm', 'tale': 'Es windet seer'}
        nid = self.tb.setlist(data, xlistid='20')
        self.assertTrue(nid == '20')

    def test_222_set_list(self):
        """ set
        Insert im dict """
        data = {'tell': 'regen', 'tale': 'it\'s raining cats and dogs'}
        nid = self.tb.setlist(data, xlistid='20')
        self.assertTrue(nid == '20')


    def test_224_set_list(self):
        """ set
        Insert im dict """
        data = {'tell': 'schnee', 'tale': 'weisser pflaum liegt auf dem zaunpfosten'}
        nid = self.tb.setlist(data, xlistid='20')
        self.assertTrue(nid == '20')

    #
    # diverse 2
    #

    def test_230_count(self):
        """ diverses
        Anzahl der vorhandenen Datensätze
        """
        dd = self.tb.count()
        self.assertTrue(dd > 0)

    def test_231_exist(self):
        """ diverses
        Sind Datensätze vorhanden
        """
        dd = self.tb.exist()
        self.assertTrue(dd)

    #
    # get
    #

    def test_240_get01(self):
        """ get
        Ein vorhandener Datensatz """
        dd = self.tb.get('4711')
        self.assertIsNotNone(dd)
        assert dd['name'] == 'roland'
        assert dd['alter'] == 54
        assert dd['id'] == '4711'

    def test_241_get02(self):
        """ get
        Einen nicht vorhandener Datensatz
        :return:
        """
        dd = self.tb.get('515151515151515')
        self.assertIsNone(dd)

    def test_244_change(self):
        """ change
        daten ändern und wieder lesen """
        dd = self.tb.get('4711')
        self.assertIsNotNone(dd)

        dd['alter'] = 60
        nic = self.tb.set(dd, '4711')
        self.assertTrue(nic == '4711')

    def test_245_get03(self):
        """ get
        Ein vorhandener Datensatz """
        dd = self.tb.get('4711')
        self.assertIsNotNone(dd)
        assert dd['name'] == 'roland'
        assert dd['alter'] == 60
        assert dd['id'] == '4711'

    def test_250_remove(self):
        """ delete
        datensatz löschen """
        nic = self.tb.rem('4711b')
        self.assertTrue(nic)
        dd = self.tb.get('4711b')
        self.assertIsNone(dd)
        a = 0


    #
    # - getlist
    #
    def test_260_getlist(self):
        """ getlist
            liest das gesamte array der liste
        """
        dd = self.tb.getlist('20')
        self.assertEqual(dd[2]['tell'], 'regen')

    def test_261_getlist(self):
        """ getlist
            Eine Liste definiert mit Key('20') und Array-Pos(0)
        """
        dd = self.tb.getlist('20', 0)
        self.assertEqual(dd['id'], '101')
        self.assertEqual(dd['tell'], 'gewitter')
        self.assertEqual(len(dd), 3, "Anzahl ")

    def test_262_getlist(self):
        """ getlist
            mit key und array key
        """
        dd = self.tb.getlist('20', '101')
        self.assertEqual(dd['id'], '101')
        a=0

    # def test_265_getlist(self):
    #     """ getlist
    #         Eine Liste definiert mit Key('20') und Array-Pos(12121220)
    #         Array-Pos ist falsch
    #     """
    #     try:
    #         dd = self.tb.getlist('20', 12121220)
    #     except Exception as ex:
    #         a=1
    #     # self.ass
    #     assert len(dd) == 3
    # IndexError: list index out of range


    #
    # - getkeys
    #

    #
    # - getall
    #

    #
    # - getfirst
    #

    #
    # - getlast
    #

    #
    # - getlistlast
    #






    #
    # ende
    #

    def test_999(self):
        """
        Aufräumen
        """
        pass


if __name__ == '__main__':
    unittest.main(verbosity=10)

