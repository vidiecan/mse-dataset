#! /usr/bin/python

"""
	Tool which creates unique mappings between
	data <-> unique ids
	queries <-> unique ids
	based on the file name.

	Changed: 2010/07/15 by jozef
"""

from __future__ import with_statement

import sys, os
from optparse import OptionParser
import mse

def is_true (val1):
	"""
		Because we try to be user friendly few inconveniences occur due to using only string type for params.
	"""
	return val1.lower() == "true"
	

# parameters like this to be user friendly
params = {
	"do_query"			: "False",
	"do_data" 			: "False",
	"do_query_files": "False",
	"path"				 	: "./",
}

# handle parameters
if len (sys.argv) > 1:
	parser = OptionParser ()
	parser.add_option ("-q", "--query", 
		   							 action="store_true", dest="do_query", default=params["do_query"],
		   							 help="create mapping for queries") 
	parser.add_option ("-f", "--query-files", 
		   							 action="store_true", dest="do_query_files", default=params["do_query_files"],
		   							 help="create query files from one file") 
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

mapping_dir = os.path.join (params["path"], mse.settings["mapping_dir"])

# do the actual stuff
if is_true(params["do_data"]):

	print "Performing data ids."
	mapping_file = os.path.join (mapping_dir, mse.settings["mapping_documents_file"])
	data_dir = os.path.join (params["path"], mse.settings["data_dir"])
	mse.create_ids (input_dir=data_dir, output_file=mapping_file)


elif is_true(params["do_query"]):

	print "Performing query ids."
	mapping_file = os.path.join (mapping_dir, mse.settings["mapping_query_file"])
	data_dir = os.path.join (params["path"], mse.settings["query_dir"])
	mse.create_ids (input_dir=data_dir, output_file=mapping_file, regexp=r".*\.xml")


elif is_true(params["do_query_files"]):

	print "Performing extraction of query files"
	query_dir = os.path.join (params["path"], mse.settings["query_dir"])
	query_summary = os.path.join (query_dir, mse.settings["query_file_summary"])
	if not os.path.exists (query_summary):
		print "Query summary not found: ", query_summary
		sys.exit ()
	
	import xml.dom.minidom

	def write_mathml (file, name, math):
		"""
			Helper method for creating valid mathml documents with only one query
		"""

		# header
		file.write (
			'<html xmlns="http://www.w3.org/1999/xhtml">\n'+
			" <head><title>Mathml MSE-Dataset query - %s</title></head>\n"%name+
			" <body>\n")
		#xml
		math.writexml (file) 
		# footer
		file.write ("\n </body>\n</html>\n")

	try:
		dom = xml.dom.minidom.parse (query_summary)	
		queries = dom.getElementsByTagName ("math")
		print "Found %d queries" % len(queries)
		i = 0
		for q in queries:
			i += 1
			file_name = "query-%d.xml" % i
			with open (os.path.join (query_dir, file_name), "w+") as f:
				write_mathml (f, file_name, q)

	except:
		mse.print_exception ("Error in processing xml file %s" % query_summary)
	


