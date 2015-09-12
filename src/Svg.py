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

import os
from OpenGL.GL import *
from numpy import reshape, dot, transpose, identity, zeros, float32
from math import sin, cos

import Log
import Config
from Texture import Texture


class ImgContext:
    def __init__(self, geometry):
        self.geometry = geometry
        self.transform = ImgTransform()
        self.setGeometry(geometry)
        self.setProjection(geometry)

        # eat any possible OpenGL errors -- we can't handle them anyway
        try:
            glMatrixMode(GL_MODELVIEW)
        except:
            Log.warn("Image renderer initialization failed; expect corrupted graphics. " +
                     "To fix this, upgrade your OpenGL drivers and set your display " +
                     "to 32 bit color precision.")

    def setGeometry(self, geometry = None):

        x, y, w, h = geometry

        glViewport(int(x), int(y), int(w), int(h))

        self.transform.reset()
        self.transform.scale(geometry[2] / 640.0, geometry[3] / 480.0)

    def setProjection(self, geometry = None):
        geometry = geometry or self.geometry

        left = geometry[0]
        right = geometry[0] + geometry[2]
        bottom = geometry[1]
        top = geometry[1] + geometry[3]

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(left, right, bottom, top, -100, 100)
        glMatrixMode(GL_MODELVIEW)

        self.geometry = geometry


    def clear(self, r = 0, g = 0, b = 0, a = 0):
        glDepthMask(1)
        glEnable(GL_COLOR_MATERIAL)
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT | GL_STENCIL_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

class ImgTransform:
    def __init__(self, baseTransform = None):
        self.reset()

        if baseTransform:
            self.matrix = baseTransform.matrix.copy()

    def transform(self, transform):
        self.matrix = dot(self.matrix, transform.matrix)

    def reset(self):
        self.matrix = identity(3, float32)

    def translate(self, dx, dy):
        m = zeros((3, 3))
        m[0, 2] = dx
        m[1, 2] = dy
        self.matrix += m

    def rotate(self, angle):
        m = identity(3, float32)
        s = sin(angle)
        c = cos(angle)
        m[0, 0] =  c
        m[0, 1] = -s
        m[1, 0] =  s
        m[1, 1] =  c
        self.matrix = dot(self.matrix, m)

    def scale(self, sx, sy):
        m = identity(3, float32)
        m[0, 0] = sx
        m[1, 1] = sy
        self.matrix = dot(self.matrix, m)

    def applyGL(self):
        # Interpret the 2D matrix as 3D
        m = self.matrix
        m = [m[0, 0], m[1, 0], 0.0, 0.0,
             m[0, 1], m[1, 1], 0.0, 0.0,
                 0.0,     0.0, 1.0, 0.0,
             m[0, 2], m[1, 2], 0.0, 1.0]
        glMultMatrixf(m)

class ImgDrawing:
    def __init__(self, context, imgPath):
        self.imgPath = None
        self.texture = None
        self.context = context
        self.cache = None
        self.transform = ImgTransform()

        # Load PNG files directly
        if imgPath.endswith(".png"):
            self.texture = Texture(imgPath)
        else:
            e = "Unsupported Image format."
            Log.error(e)
            raise RuntimeError(e)

        # Make sure we have a valid texture
        if not self.texture:
            e = "Unable to load texture for %s." % imgPath
            Log.error(e)
            raise RuntimeError(e)

    def convertToTexture(self, width, height):
        if self.texture:
            return

        e = "Img drawing does not have a valid texture image."
        Log.error(e)
        raise RuntimeError(e)

    def _getEffectiveTransform(self):
        transform = ImgTransform(self.transform)
        transform.transform(self.context.transform)
        return transform

    def draw(self, color = (1, 1, 1, 1)):
        glMatrixMode(GL_TEXTURE)
        glPushMatrix()
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        self.context.setProjection()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        transform = self._getEffectiveTransform()
        if self.texture:
            glLoadIdentity()
            transform.applyGL()

            glScalef(self.texture.pixelSize[0], self.texture.pixelSize[1], 1)
            glTranslatef(-.5, -.5, 0)
            glColor4f(*color)

            self.texture.bind()
            glEnable(GL_TEXTURE_2D)
            glBegin(GL_TRIANGLE_STRIP)
            glTexCoord2f(0.0, 1.0)
            glVertex2f(0.0, 1.0)
            glTexCoord2f(1.0, 1.0)
            glVertex2f(1.0, 1.0)
            glTexCoord2f(0.0, 0.0)
            glVertex2f(0.0, 0.0)
            glTexCoord2f(1.0, 0.0)
            glVertex2f(1.0, 0.0)
            glEnd()
            glDisable(GL_TEXTURE_2D)
        glMatrixMode(GL_TEXTURE)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
