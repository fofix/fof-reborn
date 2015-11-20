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

import sys
import os
VERSION = '1.3'

def appName():
    return "fretsonfire"

def revision():
    return int("$LastChangedRevision: 110 $".split(" ")[1])

def version():
    return "%s.%d" % (VERSION, revision())

def dataPath():
    # Determine whether were running from an exe or not

    if hasattr(sys, "frozen"):
        if os.name == "posix":
            dataPath = os.path.join(os.path.dirname(sys.argv[0]), "../lib/fretsonfire")
            if not os.path.isdir(dataPath):
                dataPath = "data"
        else:
            dataPath = "data"
    else:
        # recurse up until we find the data directory
        pathTimes = []
        while True:
            path = os.path.abspath(os.path.join(*(pathTimes+['data'])))
            if os.path.exists(path):
                dataPath = path
                break
            else:
                pathTimes.append('..')
    return dataPath
