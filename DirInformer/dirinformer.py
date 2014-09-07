#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projekt : cosa
  
       File : dirinformerr
      Datum : 16.07.14
      Autor : rkruggel
  Copyright : Roland Kruggel, 2014
  
  Bescheibung:
   ...
"""
import time

__author__ = 'rkruggel'

import sys
import os
import subprocess
import datetime


PROG = 'Sublime\ Text\ 2.app'
DIRINFO_FILE = 'README.dinf'

fi = sys.argv

header_list = []
new_list = []
old_list = []


def getEditor():
    """Ermittel den Editor für verschiedene Betriebsysteme
    """
    pd, prog, pf = None, None, None

    if sys.platform.startswith('darwin'):
        pd = '/Applications'
        prog = PROG
        pf = 'Contents/MacOS/' + os.path.splitext(prog)[0]
    elif sys.platform.startswith('win'):
        pd = '/Programme'
        prog = PROG
    elif sys.platform.startswith('linux'):
        pd = '/usr/bin'
        prog = PROG

    if pf:
        fullprog = os.path.join(pd, prog, pf)
    else:
        fullprog = os.path.join(pd, prog)

    return fullprog


def getFilepath():
    """
    :return: string filedir
    """
    bb = os.path.normpath(os.getcwd()).replace(' ', '\\ ')
    return bb


def getFullfilename():
    """ Ermittelt den Filenamen

    :return: string Full Filename
    """
    bb = None
    if len(fi) > 1:
        # bb = os.path.abspath(fi[1]).replace(' ', '\ ')
        # bb = os.path.join(getFilepath(), fi[1])
        bb = fi[-1]
    return bb


def readReadme():
    """ Liest die 'README.dinf'  und initialisiert sie wenn notwendig.
    Es wird eine eindeutige Kennung am anfang geschrieben und diese Datei
    als 'README.dinf' zu kennzeichnen. Die Kennzeichnung ist die Zeichenfolge
    ## README.DINF ## in der ersten Zeile.

    :return: string Die gekennzeichnete Datei.
    """
    global header_list, old_list

    try:
        fn = getFullfilename()
        f = open(fn)
        rlist = f.readlines()
        f.close()
    except Exception, e:
        rlist = []

    for ii in range(0, len(rlist)):
        rlist[ii] = rlist[ii].strip()

    # -- header erstellen.
    #    Der Header wird immer neu erstellt
    header_list = [
        '## README.DINF ##',
        'Path: ' + getFilepath(),
        'Datum: ' + datetime.date.today().isoformat()
    ]

    # -- Header/Rest abspalten
    for ii in rlist:
        if ii.startswith('D:') or ii.startswith('F:'):
            old_list.append(ii)

    return True


def setPathDate(rlist):
    """Setzt die Pfad und datum in der README.dinf
    """
    # for ii in range(0, len(new_list)):
    # n = new_list[ii]
    # if n.startswith('Path:'):
    #         new_list[ii] = 'Path: ' + getFilepath() + '\n'
    #     if n.startswith('Datum'):
    #         new_list[ii] = 'Datum: ' + str(time.time()) + '\n'

    return rlist


def saveReadme(rlist):
    """ Liest die 'README.dinf'  und initialisiert sie wenn notwendig.
    Es wird eine eindeutige Kennung am anfang geschrieben und diese Datei
    als 'README.dinf' zu kennzeichnen. Die Kennzeichnung ist die Zeichenfolge
    ## README.DINF ## in der ersten Zeile.

    :return: string Die gekennzeichnete Datei.
    """
    f = open(getFullfilename(), 'w')
    for ii in header_list:
        f.write(ii + '\n')
    f.write('\n')
    for ii in new_list:
        f.write(ii + '\n')
    f.close()

    return True


def readDir(dirname):
    """ Liest das aktuelle Verzeichnis und erstellt eine Liste von Dir's und File's

    :return: string Die gekennzeichnete Datei
    """
    global new_list, old_list
    a = 0
    # from os.path import join, getsize

    for root, dirs, files in os.walk(dirname):
        # print root, "consumes",
        # print sum(getsize(join(root, name)) for name in files),
        # print "bytes in", len(files), "non-directory files"

        for ii in ['CVS', '.DS_Store', 'README.dinf']:
            if ii in dirs:
                dirs.remove(ii)  # don't visit CVS directories
            if ii in files:
                files.remove(ii)  # don't visit CVS directories

        for ii in dirs:
            new_list.append('D: ' + ii + ':')

        for ii in files:
            new_list.append('F: ' + ii + ':')

        break

    nlist = list(set(old_list + new_list))
    nlist.sort()
    new_list = nlist

    a = 0


if len(fi) == 1:
    subprocess.call(["echo 'muss mit file aufgerufen werden'"], stdout=subprocess.PIPE, shell=True)
    exit()


if __name__ == "__main__":

    a = 0

    x1 = readReadme()

    readDir('.')
    jd2 = saveReadme(new_list)

    a = 0

    cc = getEditor() + ' ' + getFullfilename()

    p = subprocess.Popen(cc, shell=True, stdout=subprocess.PIPE)
    # p = subprocess.Popen('cat ' + bb, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()

    # p.wait()

    a = 0

    # list(set(listone + listtwo))
