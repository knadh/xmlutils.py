"""
    xml2csv.py
    Kailash Nadh, http://nadh.in
    October 2011
    
    License:        MIT License
    Documentation:    http://nadh.in/code/xmlutils.py
"""

import argparse
import codecs
import xml.etree.ElementTree as et

print """xml2csv.py by Kailash Nadh (http://nadh.in)
--help for help

"""

# parse arguments
parser = argparse.ArgumentParser(description='Convert an xml file to csv format.')
parser.add_argument('--input', dest='input_file', required=True, help='input xml filename')
parser.add_argument('--output', dest='output_file', required=True, help='output csv filename')
parser.add_argument('--tag', dest='tag', required=True, help='the record tag. eg: item')
parser.add_argument('--delimiter', dest='delimiter', default=', ', help='delimiter character. (default=, comma-space)')
parser.add_argument('--ignore', dest='ignore', default='', nargs='+', help='list of tags to ignore')
parser.add_argument('--header', dest='header', type=int, default=1, help='print csv header (1=yes, 0=no)? (default=1)')
parser.add_argument('--encoding', dest='encoding', default='utf-8', help='character encoding (default=utf-8)')
parser.add_argument('--limit', type=int, dest='limit', default=-1, help='maximum number of records to process')
parser.add_argument('--buffer', type=int, dest='buffer', default='1000', help='number of records to keep in buffer before writing to disk (default=1000)')
args = parser.parse_args()

# output file handle
output = codecs.open(args.output_file, "w", encoding=args.encoding)

# open the xml file for iteration
context = et.iterparse(args.input_file, events=("start", "end"))
context = iter(context)

# get to the root
event, root = context.next()

items = []
tags = []
output_buffer = []

tagged = False
started = False
n = 0


def write_buffer():
    """
    Write records from buffer to the output file
    """
    global output_buffer, output
    
    output.write('\n'.join(output_buffer) + '\n')
    output_buffer = []
    
    print ".",


def show_stats():
    print "\n\nWrote", n, "records to", args.output_file

# iterate through the xml
for event, elem in context:
    if event == 'start' and elem.tag == args.tag and not started:
        started = True

    elif event == 'end':
        if started and elem.tag != args.tag and elem.tag not in args.ignore:  # child nodes of the specified record tag
            if not tagged:
                tags.append(elem.tag)  # add tag name to csv header
            items.append('' if elem.text is None else elem.text.strip().replace('"', r'\"'))

        # end of traversing the record tag
        elif elem.tag == args.tag and len(items) > 0:
            # csv header (element tag names)
            if args.header == 1 and not tagged:
                output.write('#' + args.delimiter.join(tags) + '\n')
            tagged = True

            # send the csv to buffer
            output_buffer.append(r'"' + (r'"' + args.delimiter + r'"').join(items) + r'"')
            items = []
            n += 1

            # halt if the specified limit has been hit
            if n == args.limit:
                break

            # flush buffer to disk
            if len(output_buffer) > args.buffer:
                write_buffer()

        elem.clear()  # discard element and recover memory

write_buffer()
show_stats()
