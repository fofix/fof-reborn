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

from View import BackgroundLayer
from Input import KeyListener
from Camera import Camera
import Player

from OpenGL.GL import *
from OpenGL.GLU import *

class Scene(BackgroundLayer, KeyListener):
    def __init__(self, engine):
        self.engine  = engine
        self.camera  = Camera()
        self.time    = 0.0
        self.player = self.engine.world.getPlayers()[0]
        self.controls = Player.Controls()

    def shown(self):
        self.engine.input.addKeyListener(self)

    def hidden(self):
        self.engine.input.removeKeyListener(self)

    def keyPressed(self, key, unicode):
        c = self.controls.keyPressed(key)
        if c:
            return True
        return False

    def keyReleased(self, key):
        c = self.controls.keyReleased(key)
        if c:
            return True
        return False

    def run(self, ticks):
        self.time += ticks / 50.0

    def render3D(self):
        pass

    def render(self, visibility, topMost):
        font = self.engine.data.font

        # render the scene
        try:
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            gluPerspective(60, self.engine.view.aspectRatio, 0.1, 1000)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

            glPushMatrix()
            self.camera.apply()

            self.render3D()
        finally:
            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
