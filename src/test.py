#! /usr/bin/python 

from log_parser_v1 import log_parse
import os, sys

log_file_name = "%s/l1rp.0"%os.getcwd()

log_parse(log_file_name)

