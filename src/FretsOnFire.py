#!/usr/bin/python
# -*- coding: utf-8 -*-

#####################################################################
# Frets on Fire                                                     #
# Copyright (C) 2006 Sami Kyöstilä                                  #
#                                                                   #
# This program is free software; you can redistribute it and/or     #
# modify it under the terms of the GNU General Public License       #
# as published by the Free Software Foundation; either version 2    #
# of the License, or (at your option) any later version.            #
#                                                                   #
# This program is distributed in the hope that it will be useful,   #
# but WITHOUT ANY WARRANTY; without even the implied warranty of    #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the     #
# GNU General Public License for more details.                      #
#                                                                   #
# You should have received a copy of the GNU General Public License #
# along with this program; if not, write to the Free Software       #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,        #
# MA  02110-1301, USA.                                              #
#####################################################################

"""
Main game executable.
"""
import sys
import os
import platform
import subprocess
import atexit

def run_command(command):
    command = command.split(' ')
    cmd = subprocess.Popen(command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE)

    output, err = cmd.communicate()
    data = output.strip()

    return data

# This prevents the following message being displayed on osx:
# ApplePersistenceIgnoreState: Existing state will not be touched. New state will be written to *path*
if 'Darwin' in platform.platform():
    data = run_command('defaults read org.python.python ApplePersistenceIgnoreState')

    if data in ['1', 'ON']:
        run_command('defaults write org.python.python ApplePersistenceIgnoreState 0')
        atexit.register(run_command, 'defaults write org.python.python ApplePersistenceIgnoreState %s' % data)

# This trickery is needed to get OpenGL 3.x working with py2exe
if hasattr(sys, "frozen") and os.name == "nt":
    import ctypes
    from ctypes import util
    sys.path.insert(0, "data/PyOpenGL-3.0.0a5-py2.5.egg")
    sys.path.insert(0, "data/setuptools-0.6c8-py2.5.egg")

# Register the latin-1 encoding
import codecs
import encodings.iso8859_1
import encodings.utf_8
codecs.register(lambda encoding: encodings.iso8859_1.getregentry())
codecs.register(lambda encoding: encodings.utf_8.getregentry())
assert codecs.lookup("iso-8859-1")
assert codecs.lookup("utf-8")

import Resource
from fretwork import log
logFile = open(os.path.join(Resource.getWritableResourcePath(), "fretsonfire.log"), 'w')
log.setLogfile(logFile)

import fretwork
fretworkRequired = (0, 2, 0)
reqVerStr = '.'.join([str(i) for i in fretworkRequired])
fretworkErrorStr = '''

The version of fretwork installed is old. Please install the latest version from github.
https://github.com/fofix/fretwork/releases/
Installed: {0}
Required: {1}
'''
if getattr(fretwork, '__version__'): # The first version of fretwork didnt have __version__
    version, verType = fretwork.__version__.split('-') # remove 'dev' from ver
    version = tuple([int(i) for i in version.split('.')])

    if version < fretworkRequired:
        fwErrStr = fretworkErrorStr.format(fretwork.__version__, reqVerStr)
        raise RuntimeError(fwErrStr)

else:
    version = '0.1.0'
    fwErrStr = fretworkErrorStr.format(version, reqVerStr)
    raise RuntimeError(fwErrStr)

from GameEngine import GameEngine
from MainMenu import MainMenu
import Config
import Version
import getopt

usage = """%(prog)s [options]
Options:
  --verbose, -v         Verbose messages
  --play, -p [songName] Start playing the given song
""" % {"prog": sys.argv[0] }

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vp:", ["verbose", "play="])
    except getopt.GetoptError:
        print usage
        sys.exit(1)

    songName = None
    for opt, arg in opts:
        if opt in ["--verbose", "-v"]:
            log.quiet = False
        elif opt in ["--play", "-p"]:
            songName = arg

    while True:
        config = Config.load(Version.appName() + ".ini", setAsDefault = True)
        engine = GameEngine(config)
        menu   = MainMenu(engine, songName = songName)
        engine.setStartupLayer(menu)

        try:
            while engine.run():
                pass
        except KeyboardInterrupt:
            pass

        if engine.restartRequested:
            log.notice("Restarting.")

            try:
            # Determine whether were running from an exe or not
                if hasattr(sys, "frozen"):
                    if os.name == "nt":
                        os.execl("FretsOnFire.exe", "FretsOnFire.exe", *sys.argv[1:])
                    elif sys.platform == "darwin":
                        # This exit code tells the launcher script to restart the game
                        sys.exit(100)
                    else:
                        os.execl("./FretsOnFire", "./FretsOnFire", *sys.argv[1:])
                else:
                    if os.name == "nt":
                        bin = "c:/python25/python"
                    else:
                        bin = "/usr/bin/python"
                    os.execl(bin, bin, "FretsOnFire.py", *sys.argv[1:])
            except:
                log.warn("Restart failed.")
                raise
            break
        else:
            break
    engine.quit()
