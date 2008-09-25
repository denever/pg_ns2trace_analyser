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
from threading import Thread
from tracesql import create_db_from_trace

class FileManager(gobject.GObject, Thread):
    def __init__(self):
        Thread.__init__(self)
        self.to_open_files = []
#        self.to_remove_files = []
        
    def open_tracefile(self, db_filename, trace_filename):
        self.to_open_files.append((db_filename, trace_filename))
    
#    def open_db(self,  db_filename):
#        self.to_open_files.append((db_filename, None))
        
#    def remove_db(self, db_filename):
#        self.to_remove_files.append(db_filename)
        
    def run(self):
        while 1:
            if len(self.to_open_files):
                (db_filename, trace_filename) = self.to_open_files.pop()
                print 'opening',trace_filename,'in',db_filename
                create_db_from_trace(db_filename, trace_filename)
                # emit signal
                
#            if len(self.to_remove_files):
#                os.remove(self.to_remove_files.pop())
#                # emit signal
