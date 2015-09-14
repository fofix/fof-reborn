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

import pygame
import Log
import time
import sys
from Task import Task

# Yeah, py2exe is weird...
if hasattr(sys, "frozen"):
    import pygame.mixer_music
    pygame.mixer.music = sys.modules["pygame.mixer_music"]

# Pyglet-based audio is still experimental at the moment
#import pyglet

# OGG support disabled due to incompatibility with Python 2.5
#try:
#  import ogg.vorbis
#except ImportError:
#  Log.warn("PyOGG not found. OGG files will be fully decoded prior to playing; expect absurd memory usage.")

class Audio(Task):
    def __init__(self):
        Task.__init__(self)

    def pre_open(self, frequency = 22050, bits = 16, stereo = True, bufferSize = 1024):
        pygame.mixer.pre_init(frequency, -bits, stereo and 2 or 1, bufferSize)
        return True

    def open(self, frequency = 22050, bits = 16, stereo = True, bufferSize = 1024):
        try:
            pygame.mixer.quit()
        except:
            pass

        try:
            pygame.mixer.init(frequency, -bits, stereo and 2 or 1, bufferSize)
        except:
            Log.warn("Audio setup failed. Trying with default configuration.")
            pygame.mixer.init()

        Log.debug("Audio configuration: %s" % str(pygame.mixer.get_init()))
        return True

    def getChannelCount(self):
        return pygame.mixer.get_num_channels()

    def getChannel(self, n):
        return Channel(n)

    def close(self):
        # PyGame crashes on mac if you do this
        if sys.platform != "darwin":
            pygame.mixer.quit()

    def pause(self):
        pygame.mixer.pause()

    def unpause(self):
        pygame.mixer.unpause()

class Music(object):
    def __init__(self, fileName):
        pygame.mixer.music.load(fileName)

    @staticmethod
    def setEndEvent(event):
        pygame.mixer.music.set_endevent(event)

    def play(self, loops = -1, pos = 0.0):
        pygame.mixer.music.play(loops, pos)

    def stop(self):
        pygame.mixer.music.stop()

    def rewind(self):
        pygame.mixer.music.rewind()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def setVolume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def fadeout(self, time):
        pygame.mixer.music.fadeout(time)

    def isPlaying(self):
        return pygame.mixer.music.get_busy()

    def getPosition(self):
        return pygame.mixer.music.get_pos()

class Channel(object):
    def __init__(self, id):
        self.channel = pygame.mixer.Channel(id)

    def play(self, sound):
        self.channel.play(sound.sound)

    def stop(self):
        self.channel.stop()

    def setVolume(self, volume):
        self.channel.set_volume(volume)

    def fadeout(self, time):
        self.channel.fadeout(time)

class Sound(object):
    def __init__(self, fileName):
        self.sound   = pygame.mixer.Sound(fileName)

    def play(self, loops = 0):
        self.sound.play(loops)

    def stop(self):
        self.sound.stop()

    def setVolume(self, volume):
        self.sound.set_volume(volume)

    def fadeout(self, time):
        self.sound.fadeout(time)

# OGG files will be fully decoded prior to playing; expect absurd memory usage.
# PyOGG support has been removed this will be fixed in the future.
class StreamingSound(Sound, Task):
    def __init__(self, engine, channel, fileName):
        Sound.__init__(self, fileName)

