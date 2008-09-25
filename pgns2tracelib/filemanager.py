#! /usr/bin/env python
# -*- Python -*-
###########################################################################

#                        --------------------                             #

#  copyright            : Giuseppe "denever" Martino                      #
#  email                : denever@users.sf.net                            #
###########################################################################
###########################################################################
#                                                                         #
#   This program is free software; you can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License as published by  #
#   the Free Software Foundation; either version 2 of the License, or     #
#   (at your option) any later version.                                   #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with this program; if not, write to the Free Software            #
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,             #
#  MA 02110-1301 USA                                                      #
#                                                                         #
###########################################################################

import os
import gobject
import Queue
from threading import Thread, Event
from tracesql import create_db_from_trace

class FileManager(gobject.GObject, Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.files_to_open = Queue.Queue()
        self.evnt_new_file = Event()
        
    def open_tracefile(self, db_filename, trace_filename):
        self.files_to_open.put((db_filename, trace_filename))
        self.evnt_new_file.set()
        
    def stop(self):
        self.running = False
        self.evnt_new_file.set()
        
    def run(self):
        while self.running:
            if self.files_to_open.empty():
                self.evnt_new_file.wait()
                self.evnt_new_file.clear()

                if self.running == False:
                    break
                
            (db_filename, trace_filename) = self.files_to_open.get()
            create_db_from_trace(db_filename, trace_filename)

