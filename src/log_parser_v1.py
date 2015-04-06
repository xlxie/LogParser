#! /usr/bin/python

import os,sys

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

accu_metric_list=["l1d_cache_hit",
"l1d_cache_miss",
"l1d_cache_access",
"l1d_cache_res_fail",
"l2_cache_hit",
"l2_cache_miss",
"l2_cache_access",
"l2_cache_res_fail",
"Stall",
"W0_Idle",
"W0_Scoreboard"
]
#report_metric_list[12]

def log_parse(log_file_name):
	#call_id -> {kernel_name, items}
	raw_data_dic = {}
	#kernel_name -> call_id -> [items]
	data_dic = {}
	try:
		file_obj = open(log_file_name, "r")
	except IOError:
		print "log file %s open failed\n"
		sys.exit(1)

	global_call_id = 0
	while(1):
		
		str_line = file_obj.readline()
		if len(str_line) <= 0:
			break

		if str_line[0:len("kernel_name =")] == "kernel_name =":
			kernel_name = str_line.strip().split("=")[-1]
			global_call_id = global_call_id +1
			#print kernel_name				
			raw_data_dic[global_call_id] = {}
			raw_data_dic[global_call_id]["kernel_name"] = kernel_name
			while(1):
				str_line = file_obj.readline()
				if len(str_line) <= 0:
					break
				elif str_line.strip("\n") == "----------------------------END-of-Interconnect-DETAILS-------------------------":
					break
				
				if str_line[0:len("gpu_ipc")] == "gpu_ipc":
					tmp = 0.0
					str_item = str_line.strip().split("=")[-1]
					tmp = float(str_item)
					raw_data_dic[global_call_id][report_metric_list[0]] = tmp
				elif str_line[0:len("\tL1D_total_cache_accesses")] == "\tL1D_total_cache_accesses":
					tmp = 0.0
					str_item = str_line.strip().split("=")[-1]
					tmp = float(str_item)
					raw_data_dic[global_call_id][report_metric_list[3]] = tmp
				elif str_line[0:len("\tL1D_total_cache_misses")] == "\tL1D_total_cache_misses":
					tmp = 0.0
					str_item = str_line.strip().split("=")[-1]
					tmp = float(str_item)
					raw_data_dic[global_call_id][report_metric_list[2]] = tmp
					tmp_hit = raw_data_dic[global_call_id][report_metric_list[3]] - raw_data_dic[global_call_id][report_metric_list[2]] 
					raw_data_dic[global_call_id][report_metric_list[1]] = tmp_hit
					raw_data_dic[global_call_id][report_metric_list[5]] = tmp_hit/(raw_data_dic[global_call_id][report_metric_list[3]]+0.01)
				elif str_line[0:len("\tL1D_total_cache_reservation_fails")] == "\tL1D_total_cache_reservation_fails":
					tmp = 0.0
					str_item = str_line.strip().split("=")[-1]
					tmp = float(str_item)
					raw_data_dic[global_call_id][report_metric_list[4]] = tmp
				elif str_line[0:len("Stall:")] == "Stall:":
					str_item = str_line.split("\t")[0].split(":")[-1]
					raw_data_dic[global_call_id][report_metric_list[11]] = float(str_item)
					str_item = str_line.split("\t")[1].split(":")[-1]
					try:
						raw_data_dic[global_call_id][report_metric_list[12]] = float(str_item)
					except ValueError:
						print "log_file_name:%s"%log_file_name
						print str_line
						sys.exit(1)
					str_item = str_line.split("\t")[2].split(":")[-1]
					raw_data_dic[global_call_id][report_metric_list[13]] = float(str_item)
				elif str_line[0:len("L2_total_cache_accesses")] == "L2_total_cache_accesses":
					str_item = str_line.strip().split("=")[-1]
					raw_data_dic[global_call_id][report_metric_list[8]] = float(str_item)
				elif str_line[0:len("L2_total_cache_misses")] == "L2_total_cache_misses":
					str_item = str_line.strip().split("=")[-1]
					raw_data_dic[global_call_id][report_metric_list[7]] = float(str_item)
					raw_data_dic[global_call_id][report_metric_list[6]] = raw_data_dic[global_call_id][report_metric_list[8]] - raw_data_dic[global_call_id][report_metric_list[7]]
					raw_data_dic[global_call_id][report_metric_list[9]] = raw_data_dic[global_call_id][report_metric_list[6]]/(raw_data_dic[global_call_id][report_metric_list[8]]+0.01)

					#print raw_data_dic[global_call_id][report_metric_list[9]]
				elif str_line[0:len("L2_total_cache_reservation_fails")] == "L2_total_cache_reservation_fails":
					str_item = str_line.strip().split("=")[-1]
					raw_data_dic[global_call_id][report_metric_list[10]] = float(str_item)
	"""
	for ite1 in raw_data_dic.keys():
		print "ite1",ite1
		for ite2 in raw_data_dic[ite1].keys():
			print "\t",ite2,raw_data_dic[ite1][ite2]
	"""
	#accu
	gite = len(raw_data_dic.keys())
	while gite>1:
		for mite in accu_metric_list:
			raw_data_dic[gite][mite] = raw_data_dic[gite][mite]-raw_data_dic[gite-1][mite]

		raw_data_dic[gite][report_metric_list[5]] = raw_data_dic[gite][report_metric_list[1]]/(raw_data_dic[gite][report_metric_list[3]]+0.1)
		raw_data_dic[gite][report_metric_list[9]] = raw_data_dic[gite][report_metric_list[6]]/(raw_data_dic[gite][report_metric_list[8]]+0.1)
		gite = gite-1
	
	gite=1

	raw_data_dic[gite][report_metric_list[5]] = raw_data_dic[gite][report_metric_list[1]]/(raw_data_dic[gite][report_metric_list[3]]+0.01)
	raw_data_dic[gite][report_metric_list[9]] = raw_data_dic[gite][report_metric_list[6]]/(raw_data_dic[gite][report_metric_list[8]]+0.01)
	"""
	for ite1 in raw_data_dic.keys():
		print "ite1",ite1
		for ite2 in raw_data_dic[ite1].keys():
			print "\t",ite2,raw_data_dic[ite1][ite2]
	"""

	#trans
	gite = 1
	while gite <= len(raw_data_dic.keys()):
		lid = 0
		if raw_data_dic[gite]["kernel_name"] in data_dic.keys():
			lid = len(data_dic[raw_data_dic[gite]["kernel_name"]].keys())+1
			data_dic[raw_data_dic[gite]["kernel_name"]][lid] = {}
		else:
			lid = 1
			data_dic[raw_data_dic[gite]["kernel_name"]] = {}
			data_dic[raw_data_dic[gite]["kernel_name"]][lid] = {}
		for mite in report_metric_list:
			data_dic[raw_data_dic[gite]["kernel_name"]][lid][mite] = raw_data_dic[gite][mite]

		gite = gite + 1
	"""
	for ite1 in data_dic.keys():
		print "kernel_name",ite1
		for ite2 in data_dic[ite1].keys():
			print "\tcall_id",ite2
			for ite3 in report_metric_list:
				print "\t\t",ite3,data_dic[ite1][ite2][ite3]
	"""
	return data_dic

