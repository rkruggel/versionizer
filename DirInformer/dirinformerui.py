#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projekt : cosa
  
       File : dirinformer
      Datum : 16.07.14
      Autor : rkruggel
  Copyright : Roland Kruggel, 2014
  
  Bescheibung:
   ...
"""

__author__ = 'rkruggel'

from Tkinter import *

root = Tk()

lab = Label(root, text=u"Viel Spa\xdf mit dem Tkinter-Tutorial")
lab.pack()

but = Button(root, text="Wo ist Tommy?")
but.pack()

root.mainloop()