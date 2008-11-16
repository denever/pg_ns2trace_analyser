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

import pygtk
import gobject

pygtk.require('2.0')

import gtk
#import gobject
import threading
from decimal import Decimal

from gtk import *
from gtk import glade

from pgns2tracelib.filemanager import FileManager
from pgns2tracelib.tracemanager import TraceManager

class Gui:
    def __init__(self):
        self.fm = FileManager()
        self.tm = TraceManager()
        self.fm.start()
        self.tm.start()
        self.wtree = glade.XML('glade/traceanalyser.glade')
    	self.wtree.get_widget('win_traceanalyser').show()        
 	dict = {}
	for key in dir(self.__class__):
	    dict[key] = getattr(self, key)
	self.wtree.signal_autoconnect(dict)
        self.tm.connect('operation-completed', self.on_operation_completed)

        self.tvw_nodes = self.wtree.get_widget('tvw_nodes')

        tvc_nodes = gtk.TreeViewColumn('Id')
        cell = gtk.CellRendererText()
        tvc_nodes.pack_start(cell)
        tvc_nodes.set_attributes(cell, text=0)
        self.tvw_nodes.append_column(tvc_nodes)
        self.node_list = gtk.ListStore(str)
        self.tvw_nodes.set_model(self.node_list)
        
        self.tvw_flows = self.wtree.get_widget('tvw_flows')
        
        tvc_flowid = gtk.TreeViewColumn('FlowId')
        tvc_src = gtk.TreeViewColumn('Source')
        tvc_dst = gtk.TreeViewColumn('Destination')
        tvc_type = gtk.TreeViewColumn('Type')

        cel_flowid = gtk.CellRendererText()
        cel_src = gtk.CellRendererText()
        cel_dst = gtk.CellRendererText()
        cel_type = gtk.CellRendererText()

        tvc_flowid.pack_start(cel_flowid)
        tvc_src.pack_start(cel_src)
        tvc_dst.pack_start(cel_dst)
        tvc_type.pack_start(cel_type)
        
        tvc_flowid.set_attributes(cel_flowid, text=0)
        tvc_src.set_attributes(cel_src, text=1)
        tvc_dst.set_attributes(cel_dst, text=2)
        tvc_type.set_attributes(cel_type, text=3)
        
        self.tvw_flows.append_column(tvc_flowid)
        self.tvw_flows.append_column(tvc_src)
        self.tvw_flows.append_column(tvc_dst)
        self.tvw_flows.append_column(tvc_type)
        
        self.flow_list = gtk.ListStore(str,str,str,str)
        self.tvw_flows.set_model(self.flow_list)

        self.flt_trace = gtk.FileFilter()
        self.flt_trace.set_name('NS2 New Trace File')
        self.flt_trace.add_pattern('*.tr')
        self.flt_prj = gtk.FileFilter()
        self.flt_prj.set_name('Project Trace Analyser')
        self.flt_prj.add_pattern('*.pta')
        self.wtree.get_widget('dlg_newfile').add_filter(self.flt_trace)
        self.wtree.get_widget('dlg_openfile').add_filter(self.flt_prj)
        self.pgb_loading = self.wtree.get_widget('pgb_loading')
        self.pgb_loading.set_pulse_step(0.3)
        self.timeoutId = 0
        
    def on_mnuitm_new_activate(self, widget):
        self.wtree.get_widget('dlg_newprj').show()        
        
    def on_mnuitm_open_activate(self, widget):
        self.wtree.get_widget('dlg_openfile').show()

    def on_mnuitm_save_activate(self, widget):
        self.wtree.get_widget('dlg_savefile').show()

    def on_btn_newprj_clicked(self, widget):
        self.wtree.get_widget('dlg_newprj').hide()
        self.wtree.get_widget('dlg_newfile').show()
        
    def on_btn_new_open_clicked(self, widget):
        self.wtree.get_widget('dlg_newfile').hide()
        filename = self.wtree.get_widget('dlg_newfile').get_filename()
        newprjname = self.wtree.get_widget('ent_newprjname').get_text() + '.pta'
        self.fm.open_tracefile(newprjname, filename)
        
    def on_btn_open_clicked(self, widget):
        self.wtree.get_widget('dlg_openfile').hide()
        filename = self.wtree.get_widget('dlg_openfile').get_filename()
        self.tm.open_db(filename)
        self.wtree.get_widget('mnuitm_stats').show()
        
    def on_mnuitm_get_nodes_activate(self, widget):
        self.timeoutId = gobject.timeout_add(300,self.on_operation_running)        
    	self.wtree.get_widget('dlg_loading').show()
        self.tm.query_nodes()
        self.tm.close_operations()

#        node_ids = self.tm.get_result()
#        for node_id in node_ids:
#            self.node_list.append([node_id])
           
    def on_mnuitm_get_flows_activate(self, widget):
        self.timeoutId = gobject.timeout_add(300,self.on_operation_running)        
    	self.wtree.get_widget('dlg_loading').show()
        self.tm.query_flows()
        self.tm.query_src_dst_per_flow()
        self.tm.query_flow_types()
        self.tm.close_operations()
        
#        while 1:

#         flow_ids = self.tm.get_result()
#         flow_ids.sort()
#         flow_src_dst = self.tm.get_result()
#         flow_types = self.tm.get_result()
        
#         for flow_id in flow_ids:
#             (src,dst) = flow_src_dst[flow_id]
#             flow_type = flow_types[flow_id]
#             row = flow_id,src,dst,flow_type
#             self.flow_list.append(row)

    def on_mnuitm_avgthroughput_activate(self, widget):
        sel = self.tvw_flows.get_selection()
        model, sel_iter = sel.get_selected()
        flow_id, ip_src, ip_dst = self.flow_list.get(sel_iter,0,1,2)
        flow_id = int(flow_id)
        ip_src = int(ip_src)
        ip_dst = int(ip_dst)
        
        self.tm.query_sent_pkts_times_at(ip_src, flow_id)
        self.tm.query_recv_pkts_times_at(ip_dst, flow_id)
        self.tm.query_recv_flow_total_size_at(ip_dst, flow_id, 20)
        self.tm.close_operations()
        
        sent_pkts = self.tm.get_result()
        recv_pkts = self.tm.get_result()
        tota_size = self.tm.get_result()

        start_time = Decimal(sent_pkts[0][1])
        stop_time = Decimal(recv_pkts[-1][1])                

        delta = stop_time - start_time
        data_size = Decimal(tota_size)
        th_bps = data_size / delta
        conv = Decimal(8) / Decimal(1000)
        
        avg_tput = th_bps*conv
        
        print 'Avg tput', avg_tput

    def on_btn_open_cancel_clicked(self, widget):
        self.wtree.get_widget('dlg_openfile').hide()

    def on_btn_save_cancel_clicked(self, widget):
        self.wtree.get_widget('dlg_savefile').hide()

    def on_operation_completed(self, tm):
        self.wtree.get_widget('dlg_loading').hide()
        gobject.source_remove(self.timeoutId)        

    def on_operation_running(self):
        self.pgb_loading.pulse()
        return True
        
    def on_mnuitm_exit_activate(self, widget):
        self.tm.stop()
        self.fm.stop()
        self.tm.join()
        self.fm.join()
        gtk.main_quit()

if __name__ == "__main__":
    gobject.threads_init()
    gui = Gui()
    main()

#         flow_ids = self.trace_db.get_flows()
#         self.trace_db = NS2NewTraceSql(filename)
        
#         for node_id in self.trace_db.get_nodes():
#             self.node_list.append([node_id])

#         flow_ids = self.trace_db.get_flows()
#         flow_ids.sort()
#         flow_src_dst = self.trace_db.get_src_dst_per_flow()
#         flow_types = self.trace_db.get_flow_types()
        
#         for flow_id in flow_ids:
#             (src,dst) = flow_src_dst[flow_id]
#             flow_type = flow_types[flow_id]
#             row = flow_id,src,dst,flow_type
#             self.flow_list.append(row)

#         self.wtree.get_widget('mnuitm_stats').show()
