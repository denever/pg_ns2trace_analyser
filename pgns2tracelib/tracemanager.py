#! /usr/bin/env python
# -*- Python -*-
###########################################################################
#                           NS2NewTraceParser                             #
#                        --------------------                             #
#  copyright         (C) 2008  Giuseppe "denever" Martino                 #
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
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA#
#                                                                         #
###########################################################################

from threading import Thread
from tracesql import TraceSql
from tracesql import create_db_from_trace

class TraceManager(Thread):
    def __init__(self, db_name = None):
        Thread.__init__(self)
        self.db_name = db_name
        self.tracesql = None
        self.operations = []
        
    def open_db(self, db_name):
        self.operations(
    
