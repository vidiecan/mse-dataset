#! /usr/bin/python

"""
	Tool which creates unique mappings between
	data <-> unique ids
	queries <-> unique ids
	based on the file name.

	Changed: 2010/07/15 by jozef
"""

from __future__ import with_statement

import sys
from optparse import OptionParser
import mse

def create_data_mapping (directory):
	"""
		For every file append a pair 
		id:file
		to mappings directory.
	"""
	import traceback, os, pickle

	# prepare file names
	mapping_dir = os.path.join (directory, mse.settings["mapping_dir"])
	mapping_file = os.path.join (mapping_dir, mse.settings["mapping_documents_file"])
	data_dir = os.path.join (directory, mse.settings["data_dir"])
	if not os.path.exists (data_dir):
		print "Data directory '%s' does not exist, aborting." % data_dir
		return
	if not os.path.exists (mapping_dir):	os.mkdir (mapping_dir)

	# try to guess dataset name from the last directory or just use 'dataset'
	data_name = os.path.basename(directory).strip("\\/").strip()
	if data_name == "": data_name = "dataset"

	try:
		d = []; i = 0
		with open (mapping_file, "w+") as f:
			# write to file on the fly
			for file in os.listdir (data_dir):
				i += 1
				key = data_name+"-%d" % i
				d += (key, file)
				f.write ("%s:%s\n" % (key, file))
				print key, "--", file

		# python dump
		pickle.dump (d, open (mapping_file+".pickle", "w+"))
	except:
		mse.print_exception ("Problem with file/directory while creating data mapping, details follow:")


def is_true (val1):
	"""
		Because we try to be user friendly few inconveniences occur due to using only string type for params.
	"""
	return val1.lower() == "true"
	

# parameters like this to be user friendly
params = {
	"do_query": "False",
	"do_data" : "False",
	"path"				 : "./",
}

# handle parameters
if len (sys.argv) > 1:
	parser = OptionParser ()
	parser.add_option ("-q", "--query", 
		   							 action="store_true", dest="do_query", default=params["do_query"],
		   							 help="create mapping for queries") 
	parser.add_option ("-d", "--data", 
										 action="store_true", dest="do_data", default=params["do_data"],
										 help="create mapping for data")
	parser.add_option ("-p", "--path", 
										 action="store", dest="path", default=params["path"], type="string",
										 help="directory which contains data and query directories used for creating the mapping")
	(options, args) = parser.parse_args ()
	# ensure all options are defined in parser and update the values back to params
	params = dict (map (lambda x: (x, str(eval ("options."+x))), params.keys()))

else:
	mse.update_params_interactive (params)

mse.print_params (params)

# do the actual stuff
if is_true(params["do_data"]):
	create_data_mapping (params["path"])

















