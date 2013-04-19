"""
    xml2sql.py
    Kailash Nadh, http://nadh.in
    October 2011
    
    License:        MIT License
    Documentation:    http://nadh.in/code/xmlutils.py
"""

import argparse
import codecs
import xml.etree.ElementTree as et

print """xml2sql.py by Kailash Nadh (http://nadh.in)
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
parser.add_argument('--packet', type=float, dest='packet', default='8', help=r'maximum size of an insert query in MB. see MySQL\'s max_allowed_packet (default=8)')
args = parser.parse_args()

# output file handle
output = codecs.open(args.output_file, "w", encoding=args.encoding)

# open the xml file for iteration
context = et.iterparse(args.input_file, events=("start", "end"))
context = iter(context)

# get to the root
event, root = context.next()

items = []
fields = []
output_buffer = []
field_name = ''

tagged = False
started = False

sql_len = 0
sql_insert = None
num_insert = 0
n = 0

packet_size = 0
max_packet = 1048576 * args.packet


def write_buffer():
    """
    Write records from buffer to the output file
    """
    global output_buffer, sql_insert, output, num_insert

    output.write(sql_insert + 'VALUES\n' + ', \n'.join(output_buffer) + ';\n\n')
    output_buffer = []
    num_insert += 1

    print ".",


def show_stats():
    print "\n\nWrote", n, "records to", args.output_file, " (INSERT queries =", num_insert, ")"


# iterate through the xml
for event, elem in context:
    # if elem is an unignored child node of the record tag, it should be written to buffer
    should_write = elem.tag != args.tag and started and elem.tag not in args.ignore
    # and if the user wants a fields and we have not created one yet, we should tag it too
    should_tag = not tagged and should_write

    if event == 'start':
        if elem.tag == args.tag and not started:
            started = True
        elif should_tag:
            # if elem is nested inside a "parent", field name becomes parent_elem
            field_name = '_'.join((field_name, elem.tag)) if field_name else elem.tag

    else:
        if should_write:
            if should_tag:
                fields.append(field_name)  # add field name to csv header
                # remove current tag from the tag name chain
                field_name = field_name.rpartition('_' + elem.tag)[0]
            if elem.text is None or elem.text.strip() == '':
                items.append('-')
            else:
                items.append(elem.text.replace('"', r'\"').replace('\n', r'\n').replace('\'', r"\'"))

        # end of traversing the record tag
        elif elem.tag == args.tag and len(items) > 0:
            tagged = True

            if sql_insert is None:
                sql_insert = 'INSERT INTO ' + args.table + ' (' + ','.join(fields) + ')\n'
            sql = r'("' + r'", "'.join(items) + r'")'
            sql_len += len(sql)

            if sql_len + len(sql_insert) + 100 < max_packet:
                # store the sql statement in the buffer
                output_buffer.append(sql)
            else:
                # packet size exceeded. flush the sql and start a new insert query
                write_buffer()
                output_buffer.append(sql)
                sql_len = 0

            items = []
            n += 1

            # halt if the specified limit has been hit
            if n == args.limit:
                break

        elem.clear()  # discard element and recover memory

write_buffer()  # write rest of the buffer to file
show_stats()
