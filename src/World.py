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

from Player import Player
import SceneFactory

STARTUP_SCENE = "SongChoosingScene"

class World(object):
    def __init__(self, engine):
        self.engine = engine
        self.players = []
        self.scene = None

    def finishGame(self):
        self.deleteScene(self.scene)
        for player in self.players:
            self.deletePlayer(player)

    def createPlayer(self, name):
        self.players.append(Player(name))

    def deletePlayer(self, player):
        self.players.remove(player)
        if self.scene:
            self.scene.player = None

    def deleteScene(self, scene):
        self.engine.view.popLayer(self.scene)
        self.engine.removeTask(scene)
        self.scene = None

    def startGame(self, **args):
        self.createScene(STARTUP_SCENE, **args)

    def createScene(self, name, **args):
        self.scene = SceneFactory.create(engine = self.engine, name = name, **args)
        self.engine.addTask(self.scene)
        self.engine.view.pushLayer(self.scene)

    def getPlayers(self):
        return self.players
