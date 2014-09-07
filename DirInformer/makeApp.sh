#!/bin/sh

# erstellt eine App für mac

rm -rf build dist setup.py /Applications/dirinformer.app/
py2applet --make-setup dirinformer.py
python setup.py py2app -A

echo "copy die anwendung"
cp -a dist/dirinformer.app /Applications

# app starten aus terminal
#  ./dist/MyApplication.app/Contents/MacOS/MyApplication

# To start your application normally with LaunchServices, you can use the open tool:
#  open -a dist/MyApplication.app

# info in:
#  sudo easy_install pip
#  https://pythonhosted.org/py2app/tutorial.html

