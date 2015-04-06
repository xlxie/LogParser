#! /usr/bin/python


import os,sys
from log_parser_v1 import log_parse

bm_list=[
"backprop",
"bfs",
"b+tree",
"cfd",
"hotspot",
"lud",
"nw",
"pathfinder",
"srad_v1",
"srad_v2",
"streamcluster"]


log_table=["l2rp.0","l2rp.1","l2rp.2","l2rp.6","l2rp.3","l2rp.4","l2rp.5","l2rp.7"]
log_alias=["768LRU","768MRU","768FIFO","768RANDOM","1536LRU","1536MRU","1536FIFO","1536RANDOM"]

report_metric_list=["gpu_ipc",
"l1d_cache_hit",
"l1d_cache_miss",
"l1d_cache_access",
"l1d_cache_res_fail",
"l1d_cache_hitrate",
"l2_cache_hit",
"l2_cache_miss",
"l2_cache_access",
"l2_cache_hitrate",
"l2_cache_res_fail",
"Stall",
"W0_Idle",
"W0_Scoreboard"
]

for bm_ite in bm_list:
	print "bm:%s"%bm_ite
	#chdir
	os.chdir("%s/%s"%(os.getcwd(),bm_ite))
	#parse
	output_list=[]
	log_ite=0
	while log_ite < len(log_table):
		output_list.append(log_parse(log_table[log_ite]))
		log_ite = log_ite+1
	#output_list

	kernel_list = output_list[0].keys()
	for kernel_ite in range(len(kernel_list)):
		call_end = len(output_list[0][kernel_list[kernel_ite]].keys())
		call_ite = 1
		while call_ite <= call_end:
			print "kerne_name:%s"%(kernel_list[kernel_ite])
			print "call_id:%d"%call_ite
			print "config gpu_ipc l1d_cache_hit l1d_cache_miss l1d_cache_access l1d_cache_res_fail l1d_cache_hitrate l2_cache_hit l2_cache_miss l2_cache_access l2_cache_hitrate l2_cache_res_fail Stall W0_Idle W0_Scoreboard"
			config_ite=0
			while config_ite < len(output_list):
				print log_alias[config_ite],
				for i in range(len(report_metric_list)):
					print output_list[config_ite][kernel_list[kernel_ite]][call_ite][report_metric_list[i]],

				print
				config_ite=config_ite+1

			call_ite=call_ite+1
			print "\n\n"
	print "\n\n\n"

	os.chdir("%s/.."%(os.getcwd()))

