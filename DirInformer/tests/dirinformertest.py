#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projekt : cosa
  
       File : dirinformertest
      Datum : 22.07.14
      Autor : rkruggel
  Copyright : Roland Kruggel, 2014
  
  Bescheibung:
   ...
"""
import time

import dirinformer as di

__author__ = 'rkruggel'

import unittest
import os
import shutil


class DirinformerTest(unittest.TestCase):
    README_FILE = './README.dinf'
    TEST_DIR = './testdir'

    # def setUp(self):
    # """"""
    # self.tb = self.inst_dict()
    # self.tl = self.inst_list()
    #     self.dt = time.time()
    #     self.dt100 = int(self.dt / 100)
    def setUp(self):
        pass

    #
    # def tearDown(self):
    #     """"""
    #     pass
    def tearDown(self):
        pass

    #
    # def test000(self):
    #     """ Der erste Test ist eigentlich kein test. Er löscht die DB. In
    #     diesem Fall das gesamte subdir
    #     """
    #     try:
    #         shutil.rmtree(self.DICT_PATH)
    #     except:
    #         pass
    def test000(self):
        if os.path.exists(self.README_FILE):
            os.remove(self.README_FILE)
        self.assertFalse(os.path.exists(self.README_FILE), msg="README.dinf ist nicht geloescht")

        x1 = di.readReadme()
        self.assertTrue(x1)

        x2 = str.join('', di.header_list)
        self.assertTrue(x2.startswith('## README.DINF ##Path: /Users/rkruggel/Dropbox/Develop/'))

        x3 = str.join('', di.old_list)
        self.assertTrue(len(x3) == 0)

        a = 0

    def test005_readdir(self):
        di.readDir(self.TEST_DIR)

        x1 = str.join('', di.header_list)
        self.assertTrue(x1.startswith('## README.DINF ##Path: /Users/rkruggel/Dropbox/Develop/Projekt'))

        x2 = str.join('', di.old_list)
        self.assertTrue(x2 == '')

        x3 = str.join('', di.new_list)
        self.assertTrue(x3.startswith('D: d1:D: d2:D: d3:F: f1:F: f2:F: f3:F: f4:'))

        a = 0

    def test006_readdir(self):
        di.readDir(self.TEST_DIR)

        x1 = str.join('', di.header_list)
        self.assertTrue(x1.startswith('## README.DINF ##Path: /Users/rkruggel/Dropbox/Develop/Projekt'))

        x3 = str.join('', di.new_list)
        self.assertTrue(x3.startswith('D: d1:D: d2:D: d3:F: f1:F: f2:F: f3:F: f4:'))

        a = 0

    def test999(self):
        a = 0
        pass


if __name__ == '__main__':
    unittest.main(verbosity=1)

    a = 0

