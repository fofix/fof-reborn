#####################################################################
# -*- coding: iso-8859-1 -*-                                        #
#                                                                   #
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

from OpenGL.GL import *
import math
import socket

from View import BackgroundLayer
from Menu import Menu
from Editor import Editor, Importer, GHImporter
from Credits import Credits
from Lobby import Lobby
from Language import _
import Dialogs
import Config
from fretwork import audio
import Settings

class MainMenu(BackgroundLayer):
    def __init__(self, engine, songName = None):
        self.engine              = engine
        self.time                = 0.0
        self.nextLayer           = None
        self.visibility          = 0.0
        self.songName            = songName

        self.engine.loadImgDrawing(self, "background", "keyboard.png")
        self.engine.loadImgDrawing(self, "guy",        "pose.png")
        self.engine.loadImgDrawing(self, "logo",       "logo.png")
        self.song = audio.Sound(self.engine.resource.fileName("menu.ogg"))
        self.song.setVolume(self.engine.config.get("audio", "songvol"))
        self.song.play(-1)

        editorMenu = Menu(self.engine, [
            (_("Edit Existing Song"),            self.startEditor),
            (_("Import New Song"),               self.startImporter),
            (_("Import Guitar Hero(tm) Songs"),  self.startGHImporter),
        ])

        settingsMenu = Settings.SettingsMenu(self.engine)

        mainMenu = [
            (_("Play Game"),   self.newSinglePlayerGame),
            (_("Tutorial"),    self.showTutorial),
            (_("Song Editor"), editorMenu),
            (_("Settings >"),  settingsMenu),
            (_("Credits"),     self.showCredits),
            (_("Quit"),        self.quit),
        ]
        self.menu = Menu(self.engine, mainMenu, onClose = lambda: self.engine.view.popLayer(self))

    def shown(self):
        self.engine.view.pushLayer(self.menu)

        if self.songName:
            self.newSinglePlayerGame(self.songName)

    def hidden(self):
        self.engine.view.popLayer(self.menu)

        if self.song:
            self.song.fadeout(1000)

        if self.nextLayer:
            self.engine.view.pushLayer(self.nextLayer())
            self.nextLayer = None
        else:
            self.engine.quit()

    def quit(self):
        self.engine.view.popLayer(self.menu)

    def catchErrors(function):
        def harness(self, *args, **kwargs):
            try:
                try:
                    function(self, *args, **kwargs)
                except:
                    import traceback
                    traceback.print_exc()
                    raise
            except socket.error, e:
                Dialogs.showMessage(self.engine, unicode(e[1]))
            except KeyboardInterrupt:
                pass
            except Exception, e:
                if e:
                    Dialogs.showMessage(self.engine, unicode(e))
        return harness

    def launchLayer(self, layerFunc):
        if not self.nextLayer:
            self.nextLayer = layerFunc
            self.engine.view.popAllLayers()

    def showTutorial(self):

        self.engine.startWorld()
        self.launchLayer(lambda: Lobby(self.engine, singlePlayer = True, songName = "tutorial"))
    showTutorial = catchErrors(showTutorial)

    def newSinglePlayerGame(self, songName = None):

        self.engine.startWorld()
        self.launchLayer(lambda: Lobby(self.engine, singlePlayer = True, songName = songName))
    newSinglePlayerGame = catchErrors(newSinglePlayerGame)

    def startEditor(self):
        self.launchLayer(lambda: Editor(self.engine))
    startEditor = catchErrors(startEditor)

    def startImporter(self):
        self.launchLayer(lambda: Importer(self.engine))
    startImporter = catchErrors(startImporter)

    def startGHImporter(self):
        self.launchLayer(lambda: GHImporter(self.engine))
    startGHImporter = catchErrors(startGHImporter)

    def showCredits(self):
        self.launchLayer(lambda: Credits(self.engine))
    showCredits = catchErrors(showCredits)

    def run(self, ticks):
        self.time += ticks / 50.0

    def render(self, visibility, topMost):
        self.visibility = visibility
        v = 1.0 - ((1 - visibility) ** 2)

        t = self.time / 100
        w, h, = self.engine.view.geometry[2:4]
        r = .5
        self.background.transform.reset()
        self.background.transform.translate((1 - v) * 2 * w + w / 2 + math.cos(t / 2) * w / 2 * r, h / 2 + math.sin(t) * h / 2 * r)
        self.background.transform.rotate(-t)
        self.background.transform.scale(math.sin(t / 8) + 2, math.sin(t / 8) + 2)
        self.background.draw()

        self.logo.transform.reset()
        self.logo.transform.translate(.5 * w, .8 * h + (1 - v) * h * 2 * 0)
        f1 = math.sin(t * 16) * .025
        f2 = math.cos(t * 17) * .025
        self.logo.transform.scale(1 + f1 + (1 - v) ** 3, -1 + f2 + (1 - v) ** 3)
        self.logo.draw()

        self.guy.transform.reset()
        self.guy.transform.translate(.75 * w + (1 - v) * 2 * w, .35 * h)
        self.guy.transform.scale(-.9, .9)
        self.guy.transform.rotate(math.pi)
        self.guy.draw()
