'''
	xml2sql.py
	Kailash Nadh, http://kailashnadh.name
	October 2011
	
	License:		MIT License
	Documentation:	http://kailashnadh.name/code/xmlutils.py
'''

import argparse, codecs, elementtree.ElementTree as et

print "xml2sql.py by Kailash Nadh (http://kailashnadh.name)\n--help for help\n\n"

# parse arguments
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--input', type=file, dest='input_file', required=True, help='input xml filename')
parser.add_argument('--output', dest='output_file', required=True, help='output sql filename')
parser.add_argument('--tag', dest='tag', required=True, help='the record tag. eg: item')
parser.add_argument('--table', dest='table', required=True, help='table name')
parser.add_argument('--ignore', dest='ignore', default='', nargs='+', help='list of tags to ignore')
parser.add_argument('--encoding', dest='encoding', default='utf-8', help='character encoding (default=utf-8)')
parser.add_argument('--limit', type=int, dest='limit', default=-1, help='maximum number of records to process')
parser.add_argument('--packet', type=float, dest='packet', default='8', help='maximum size of an insert query in MB. see MySQL\'s max_allowed_packet (default=8)')
args = parser.parse_args()


# output file handle
output = codecs.open(args.output_file, "w", encoding=args.encoding)

# open the xml file for iteration
context = et.iterparse(args.input_file, events=("start", "end"))
context = iter(context)
# get to the root
event, root = context.next()


max_packet = 1048576 * args.packet

items = []; tags = []; output_buffer = []
tagged = False
started = False
sql_len = 0
sql_insert = None
num_insert = 0
n = 0
packet_size = 0

# write records to the output file
def write_buffer():
	global output_buffer, sql_insert, output, num_insert
	
	output.write(  sql_insert + 'VALUES\n' + ', \n'.join(output_buffer) + ';\n\n' )
	output_buffer = []
	num_insert += 1

	print ".",

def show_stats():
	print "\n\nWrote", n, "records to", args.output_file, " (INSERT queries =", num_insert, ")"

# iterate through the xml
for event, elem in context:
	if event == 'start' and elem.tag == args.tag and not started:
		started = True

	#child nodes of the specified record tag
	if started and event == 'end' and elem.tag != args.tag and elem.tag not in args.ignore:
		tags.append(elem.tag) if tagged == False else True	# field names
		items.append( '-' if elem.text == None or elem.text.strip() == ''
						 else elem.text.replace('"', '\\\"')
									   .replace('\n', '\\n')
									   .replace('\'', '\\\'')
					)
					
	# end of traversing the record tag
	if event == 'end' and elem.tag == args.tag and len(items) > 0:
		tagged = True

		if sql_insert == None:
			sql_insert = 'INSERT INTO ' + args.table + ' (' + ','.join(tags) + ')\n'

		sql = '(\"' + ('\", \"').join(items) + '\")'
		sql_len += len(sql)
		
		# store the sql statement in the buffer
		if sql_len+len(sql_insert)+100 < max_packet:
			output_buffer.append(sql)
		else:
		# packet size exceeded. flush the sql and start a new insert query
			write_buffer()
			output_buffer.append(sql)
			sql_len = 0

		items = []
		n+=1
	
	# halt if the specified limit has been hit
	if n == args.limit:
		break


write_buffer()
show_stats()