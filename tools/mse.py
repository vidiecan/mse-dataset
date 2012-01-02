"""
 Utility class for MSE-Dataset to be consistent across tools.

 Changed: 2010/07/15 by jozef
"""

from __future__ import with_statement

"""
	Default parameters throughout utils for easy changing later.
"""
settings = {
	"mapping_dir"							: "mapping",
	"mapping_documents_file"	: "data.id",
	"mapping_query_file"			: "query.id",
	
	"data_dir"								: "data",

	"query_dir"								: "query",
	"query_file_summary"			: "queries.mathml",
}


def update_params_interactive (params):
	"""
		Iterate through params dictionary and ask the user for new value or the default will be used.

		For a bit more user friendly.
	"""
	for key in params.keys():
		val = raw_input ("Set paramter '%s' a new value (enter for default[%s]):" % (key, params[key])).strip()
		if val != "":
			params[key] = val

def print_params (params):
	"""
		Be consistent across tools.
	"""
	print 10*"-"
	print "Using these parameters", params
	print 10*"-"

def print_exception (str):
	"""
		Be consistent across tools.
	"""
	import traceback, sys
	print str
	print '-'*60
	traceback.print_exc(file=sys.stdout)
	print '-'*60
	

def create_ids (** kwargs):
	"""
		For every file from a directory optionally filtered by regular expression form a pair of
		id:file
		and store it in mappings directory.

		Input variables:
			input_directory - mandatory
			output_file	- mandatory
			regexp - optional
	"""
	import traceback, os, pickle, re

	# prepare file names
	try:
		input_dir = kwargs["input_dir"]
		output_file = kwargs["output_file"]
		output_dir = os.path.split (output_file)[0]
		regexp = kwargs["regexp"] if "regexp" in kwargs else ".*"
		regexp = re.compile (regexp)
	except:
		print_exception ("Error in create_data_mapping input parameters.")
		return

	if not os.path.exists (input_dir):
		print "Output directory '%s' does not exist, aborting." % input_dir
		return
	if not os.path.exists (output_dir):	os.mkdir (output_dir)

	# try to guess dataset name from the last directory or just use 'dataset'
	try:	
		data_name = os.path.split(input_dir)[0].strip("\\/.").strip()
	except:
		pass
	if not data_name: data_name = "dataset"

	try:
		d = []; i = 0
		with open (output_file, "w+") as f:
			# write to file on the fly
			for file in os.listdir (input_dir):
				if not regexp.match (file):
					print "Excluded file from ids:", file
					continue
				i += 1
				key = data_name+"-%d" % i
				d += (key, file)
				f.write ("%s:%s\n" % (key, file))
				print key, "--", file

		# python dump
		pickle.dump (d, open (output_file+".pickle", "w+"))
	except:
		print_exception ("Problem with file/directory while creating creating ids, details follow:")



