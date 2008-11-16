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

import gobject
import Queue
from threading import Thread, Event
from pgns2tracelib.tracesql import TraceSql
from pgns2tracelib.tracesql import create_db_from_trace

class TraceManager(Thread, gobject.GObject):
    __gsignals__ = { 
        'operation-completed' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
        }
    
    def __init__(self):
        Thread.__init__(self)
        gobject.GObject.__init__(self)
        self.db_name = None
        self.tracesql = None
        self.running = True
        self.operations = Queue.Queue()
        self.results = Queue.Queue()
        self.evnt_new_item = Event()
        self.evnt_new_rslt = Event()
        self.evnt_new_db = Event()
        
    def open_db(self, db_name):
        self.db_name = db_name
        self.evnt_new_db.set()

    def query_nodes(self):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_nodes, None) )
            self.evnt_new_item.set()
        
    def query_flows(self):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_flows, None) )
            self.evnt_new_item.set()
            
    def query_flow_types(self):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_flow_types, None) )
            self.evnt_new_item.set()
            
    def query_pkt_iptypes(self):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_pkt_iptypes, None) )
            self.evnt_new_item.set()
            
    def query_src_dst_per_flow(self):        
        if self.tracesql:
            self.operations.put( (self.tracesql.get_src_dst_per_flow, None) )
            self.evnt_new_item.set()
            
    def query_flow_types(self):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_flow_types, None) )
            self.evnt_new_item.set()
            
    def query_trace_of(self, unique_id):
        if self.tracesql:
            args = {'unique_id': unique_id}
            self.operations.put( (self.tracesql.get_trace_of, args) )
            self.evnt_new_item.set()
            
    def query_recv_pkts_num_at_node(self, node_id):
        if self.tracesql:
            args = {'node_id': node_id}            
            self.operations.put( (self.tracesql.count_recv_pkt_at_node, args) )
            self.evnt_new_item.set()
            
    def query_pkts_at_macdst(self, mac_dest):
        if self.tracesql:
            args = {'mac_dest': mac_dest}            
            self.operations.put( (self.tracesql.get_pkts_at_macdst, args) )
            self.evnt_new_item.set()
            
    def query_pkts_at_lvl(self, lvl):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_pkts_at_lvl, lvl) )                               
            self.evnt_new_item.set()
            
    def query_pkts_flowid(self, flowid, lvl):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_pkts_flowid, flowid, lvl) )
            self.evnt_new_item.set()
            
    def query_sent_pkts_times_at(self, node_id, flow_id):
        if self.tracesql:
            args = {'node_id': node_id, 'flow_id': flow_id}            
            self.operations.put( (self.tracesql.get_sent_pkts_times_at, args) )
            self.evnt_new_item.set()
            
    def query_recv_pkts_times_at(self, node_id, flow_id):
        if self.tracesql:
            args = {'node_id': node_id, 'flow_id': flow_id}                        
            self.operations.put( (self.tracesql.get_recv_pkts_times_at, args) )
            self.evnt_new_item.set()
            
    def query_recv_flow_total_size_at(self, node_id, flow_id, hdr_size):
        if self.tracesql:
            args = {'node_id': node_id, 'flow_id': flow_id, 'hdr_size': hdr_size}                                    
            self.operations.put( (self.tracesql.get_recv_flow_total_size_at, args) )
            self.evnt_new_item.set()
            
    def query_sent_bursts_per_flow(self, lvl):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_sent_bursts_per_flow, lvl) )
            self.evnt_new_item.set()
            
    def close_operations(self, operations_handler):
        args = {'operations_handler': operations_handler}
        self.operations.put( (self.operations_end, args) )
        self.evnt_new_item.set()
        
    def operations_end(self, operations_handler):
        self.emit('operation-completed', operations_handler) 
            
    def get_result(self):
#         if self.results.empty():
#             self.evnt_new_rslt.wait()
#             self.evnt_new_rslt.clear()

        return self.results.get()

    def stop(self):
        self.running = False
        self.evnt_new_item.set()

    def run(self):
        while self.running:
            if not self.tracesql:
                print 'Waiting for a db to open'                
                self.evnt_new_db.wait()
                self.tracesql = TraceSql(self.db_name)

            if self.tracesql:
                if self.operations.empty():
                    print 'Waiting for an operation'
                    self.evnt_new_item.wait()
                    
                    if self.running == False:
                        self.evnt_new_item.clear()
                        print 'Stopping thread'                        
                        break
                    
                self.evnt_new_item.clear()
                print 'A new operation arrived'
                function, args = self.operations.get()
                
                if args != None:
                    result = function(**args)
                    if result:
                        self.results.put(result)
                    self.evnt_new_rslt.set()
                else:
                    result = function()
                    if result:
                        self.results.put(result)
                    self.evnt_new_rslt.set()
                print result
        print 'Thread stopped'

gobject.type_register(TraceManager)
    
#     def query_trace_maconly_pkts(self):
#         It is possibile to select trace level (default is 'MAC')
#     def query_sent_bursts_per_node(self
# 	self.operations.put((self.tracesql.get_sent_bursts_per_node,lvl = 'MAC'):
#         It is possibile to select trace level (default is 'MAC')
#     def query_recv_bursts_per_flow(self
# 	self.operations.put((self.tracesql.get_recv_bursts_per_flow,lvl = 'MAC'):
#         It is possibile to select trace level (default is 'MAC')
#     def query_recv_bursts_per_node(self
# 	self.operations.put((self.tracesql.get_recv_bursts_per_node,lvl = 'MAC'):
#         It is possibile to select trace level (default is 'MAC')
#     def query_all_mac_dst(self):
