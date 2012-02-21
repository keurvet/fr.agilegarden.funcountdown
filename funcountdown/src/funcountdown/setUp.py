#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# source d'inspiration: http://wiki.wxpython.org/cx_freeze
# but, that not works
 
import sys, os
from cx_Freeze import setup, Executable
 
#############################################################################
# preparation des options 
path = sys.path.append(os.path.join("."))
includes = []
excludes = []
packages = []
xfiles = []
 
options = {"include_files": xfiles,
           "path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages,
           }
 
#############################################################################
# preparation des cibles
base = None
if sys.platform == "win32":
    base = "Win32GUI"
 
cible_1 = Executable(
    script = "funcountdown.py",
    base = base,
    compress = True,
    icon = None,
    )
 
 
#############################################################################
# creation du setup
setup(
    name = "funcd",
    version = "1.0",
    description = "An agile, simple and fun countdown timer to timebox professional or personal group activities like games or meetings",
    author = "Pierrick Thibault",
    options = {"build_exe": options},
    executables = [cible_1]
    )