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
from threading import Thread
from pgns2tracelib.tracesql import TraceSql
from pgns2tracelib.tracesql import create_db_from_trace

class TraceManager(Thread):
    operations = Queue.Queue()
    results = Queue.Queue()
    
    def __init__(self):
        Thread.__init__(self)
        self.db_name = None
        self.tracesql = None
        self.running = True
        
    def open_db(self, db_name):
        self.db_name = db_name

    def query_nodes(self):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_nodes, None) )
        
    def query_flows(self):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_flows, None) )

    def query_flow_types(self):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_flow_types, None) )
        
    def query_pkt_iptypes(self):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_pkt_iptypes, None) )
        
    def query_src_dst_per_flow(self):        
        if self.tracesql:
            self.operations.put( (self.tracesql.get_src_dst_per_flow, None) )

    def query_flow_types(self):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_flow_types, None) )

    def query_trace_of(self, unique_id):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_trace_of, unique_id) )

    def query_recv_pkts_num_at_node(self, node_id):
        if self.tracesql:
            self.operations.put( (self.tracesql.count_recv_pkt_at_node, node_id) )

    def query_pkts_at_macdst(self, mac_dest):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_pkts_at_macdst, mac_dest) )

    def query_pkts_at_lvl(self, lvl):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_pkts_at_lvl, lvl) )                               

    def query_pkts_flowid(self, flowid, lvl):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_pkts_flowid, flowid, lvl) )

    def query_sent_pkts_times_at(self, node_id, flow_id, lvl):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_sent_pkts_times_at, node_id, flow_id, lvl) )

    def query_recv_pkts_times_at(self, node_id, flow_id, lvl):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_recv_pkts_times_at, node_id, flow_id, lvl) )

    def query_recv_flow_total_size_at(self, node_id, flow_id, hdr_size, lvl):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_recv_flow_total_size_at, node_id, flow_id, hdr_size, lvl) )

    def query_sent_bursts_per_flow(self, lvl):
        if self.tracesql:
            self.operations.put( (self.tracesql.get_sent_bursts_per_flow, lvl) )

    def get_result():
        return results.get()

    def stop():
        self.running = False

    def run(self):
        while self.running:
            if not self.tracesql and self.db_name:
                self.tracesql = TraceSql(self.db_name)
                print 'opened db', self.db_name
                # emit opened db
            if self.tracesql:
                try:
                    operation = self.operations.get()
                except:
                    continue

                if operation[1] != None:
                    print operation[1:]
                    result = operation[0]([arg for arg in operation[1:] ])
                    results.put(result)
                else:
                    result = operation[0]()
                    results.put(result)

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
