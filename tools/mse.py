"""
 Utility class for MSE-Dataset to be consistent accross tools.

 Changed: 2010/07/15 by jozef
"""

"""
	Default parameters throughout utils for easy changing later.
"""
settings = {
	"mapping_dir"							: "mappings",
	"mapping_documents_file"	: "data.id",
	
	"data_dir"		: "data",
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
	

