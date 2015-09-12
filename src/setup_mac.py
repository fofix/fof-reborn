"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setup import *
from setuptools import setup

import sys, SceneFactory, Version
import amanith

APP = ['FretsOnFire.py']

OPTIONS = {
    'argv_emulation': True,
    'dist_dir': '../dist',
    'dylib_excludes': 'OpenGL,AGL',
    'frameworks' : '../../amanith/lib/libamanith.dylib', 
    'iconfile': '../data/icon_mac_composed.icns',
    'includes': SceneFactory.scenes,
    'excludes': ["ode",
      "unicodedata",
      "_ssl",
      "bz2",
      "email",
      "calendar",
      "bisect",
      "difflib",
      "doctest",
      "ftplib",
      "getpass",
      "gopherlib",
      "heapq",
      "macpath",
      "macurl2path",
      "GimpGradientFile",
      "GimpPaletteFile",
      "PaletteFile"
 ]
}

setup(
    version=Version.version(),
    description="Rockin' it Oldskool!",
    name="Frets on Fire",
    url="http://www.unrealvoodoo.org",
    app=APP,
    data_files=dataFiles,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
