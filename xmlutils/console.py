"""
	Kailash Nadh, http://nadh.in
	June 2013
	
	License:        MIT License
	Documentation:    http://nadh.in/code/xmlutils.py
"""

import argparse
from xmlutils.xml2sql import xml2sql
from xmlutils.xml2csv import xml2csv
from xmlutils.xml2json import xml2json

def run_xml2sql():
	print """xml2sql by Kailash Nadh (http://nadh.in)
	--help for help

	"""

	# parse arguments
	parser = argparse.ArgumentParser(description='Convert an xml file to sql.')
	parser.add_argument('--input', type=file, dest='input_file', required=True, help='input xml filename')
	parser.add_argument('--output', dest='output_file', required=True, help='output sql filename')
	parser.add_argument('--tag', dest='tag', required=True, help='the record tag. eg: item')
	parser.add_argument('--table', dest='table', required=True, help='table name')
	parser.add_argument('--ignore', dest='ignore', default='', nargs='+', help='list of tags to ignore')
	parser.add_argument('--encoding', dest='encoding', default='utf-8', help='character encoding (default=utf-8)')
	parser.add_argument('--limit', type=int, dest='limit', default=-1, help='maximum number of records to process')
	parser.add_argument('--packet', type=float, dest='packet', default='8', \
						help=r'maximum size of an insert query in MB. \
						see MySQL\'s max_allowed_packet (default=8)')

	args = parser.parse_args()

	converter = xml2sql(args.input_file, args.output_file, args.encoding)
	num = converter.convert(tag=args.tag, table=args.table, ignore=args.ignore, limit=args.limit, packet=args.packet)

	print "\n\nWrote", num['num'], "records to", args.output_file, \
		  " (INSERT queries =", num['num_insert'], ")"


def run_xml2csv():
	print """xml2csv by Kailash Nadh (http://nadh.in)
	--help for help

	"""

	# parse arguments
	parser = argparse.ArgumentParser(description='Convert an xml file to csv format.')
	parser.add_argument('--input', dest='input_file', required=True, help='input xml filename')
	parser.add_argument('--output', dest='output_file', required=True, help='output csv filename')
	parser.add_argument('--tag', dest='tag', required=True, help='the record tag. eg: item')
	parser.add_argument('--delimiter', dest='delimiter', default=',', help='delimiter character. (default=, comma-space)')
	parser.add_argument('--ignore', dest='ignore', default='', nargs='+', help='list of tags to ignore')
	parser.add_argument('--header', dest='header', action='store_false', default=True, help='print csv header (default=True)')
	parser.add_argument('--encoding', dest='encoding', default='utf-8', help='character encoding (default=utf-8)')
	parser.add_argument('--limit', type=int, dest='limit', default=-1, help='maximum number of records to process')
	parser.add_argument('--buffer_size', type=int, dest='buffer_size', default='1000',
						help='number of records to keep in buffer before writing to disk (default=1000)')

	args = parser.parse_args()

	converter = xml2csv(args.input_file, args.output_file, args.encoding)
	num = converter.convert(tag=args.tag, delimiter=args.delimiter, ignore=args.ignore,
							header=args.header, limit=args.limit, buffer_size=args.buffer_size)

	print "\n\nWrote", num, "records to", args.output_file


def run_xml2json():
	print """xml2sql by Kailash Nadh (http://nadh.in)
	--help for help

	"""

	# parse arguments
	parser = argparse.ArgumentParser(description='Convert an xml file to sql.')
	parser.add_argument('--input', type=file, dest='input_file', required=True, help='input xml filename')
	parser.add_argument('--output', dest='output_file', required=True, help='output sql filename')
	parser.add_argument('--pretty', dest='pretty', required=False, default=False, action='store_true', \
						help='pretty print? (default=False)')
	parser.add_argument('--encoding', dest='encoding', default='utf-8', help='character encoding (default=utf-8)')

	args = parser.parse_args()

	converter = xml2json(args.input_file, args.output_file, args.encoding)
	num = converter.convert(pretty=args.pretty)

	print "Wrote to", args.output_file
