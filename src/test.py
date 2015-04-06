#! /usr/bin/python 

from log_parser_v1 import log_parse
import os, sys

log_file_name = "%s/l1rp.0"%os.getcwd()

log_parse(log_file_name)

report_metric_list=["gpu_sim_cycle",
"gpu_sim_insn",
"gpu_ipc",
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
