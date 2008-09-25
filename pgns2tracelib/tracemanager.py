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

import Queue
from threading import Thread, Event
from pgns2tracelib.tracesql import TraceSql
from pgns2tracelib.tracesql import create_db_from_trace

class TraceManager(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.db_name = None
        self.tracesql = None
        self.running = True
        self.operations = Queue.Queue()
        self.results = Queue.Queue()
        self.evnt_new_item = Event()
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
            self.operations.put( (self.tracesql.get_trace_of, unique_id) )
            self.evnt_new_item.set()
            
    def query_recv_pkts_num_at_node(self, node_id):
        if self.tracesql:
            self.operations.put( (self.tracesql.count_recv_pkt_at_node, node_id) )
            self.evnt_new_item.set()
            
    def query_pkts_at_macdst(self, mac_dest):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_pkts_at_macdst, mac_dest) )
            self.evnt_new_item.set()
            
    def query_pkts_at_lvl(self, lvl):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_pkts_at_lvl, lvl) )                               
            self.evnt_new_item.set()
            
    def query_pkts_flowid(self, flowid, lvl):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_pkts_flowid, flowid, lvl) )
            self.evnt_new_item.set()
            
    def query_sent_pkts_times_at(self, node_id, flow_id, lvl):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_sent_pkts_times_at, node_id, flow_id, lvl) )
            self.evnt_new_item.set()
            
    def query_recv_pkts_times_at(self, node_id, flow_id, lvl):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_recv_pkts_times_at, node_id, flow_id, lvl) )
            self.evnt_new_item.set()
            
    def query_recv_flow_total_size_at(self, node_id, flow_id, hdr_size, lvl):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_recv_flow_total_size_at, node_id, flow_id, hdr_size, lvl) )
            self.evnt_new_item.set()
            
    def query_sent_bursts_per_flow(self, lvl):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_sent_bursts_per_flow, lvl) )
            self.evnt_new_item.set()
            
    def get_result(self):
        return self.results.get()

    def stop(self):
        self.running = False
        self.evnt_new_item.set()

    def run(self):
        while self.running:
            if not self.tracesql:
                self.evnt_new_db.wait()
                self.tracesql = TraceSql(self.db_name)

            if self.tracesql:
                if self.operations.empty():
                    self.evnt_new_item.wait()
                    self.evnt_new_item.clear()
                    
                    if self.running == False:
                        break

                operation = self.operations.get()

                if operation[1] != None:
                    result = operation[0]([arg for arg in operation[1:] ])
                    self.results.put(result)
                else:
                    result = operation[0]()
                    self.results.put(result)

                print result

    
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
