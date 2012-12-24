'''
	xml2json.py
	Kailash Nadh, http://nadh.in
	December 2012
	
	License:		MIT License
	Documentation:	http://nadh.in/code/xmlutils.py
'''

import argparse, codecs, elementtree.ElementTree as et
import json


# turn an ElementTree Element to a list
def elem2list(elem):
	block = {}

	# get the element's children
	children=elem.getchildren()

	if children:
		cur = map(elem2list, children)

		# create meaningful lists
		if elem[0].tag != elem[1].tag:		# [{a: 1}, {b: 2}, {c: 3}] => {a: 1, b: 2, c: 3}
			cur =	dict(zip(
								map(lambda e: e.keys()[0], cur),
								map(lambda e: e.values()[0], cur)
							))
		else:								# [{a: 1}, {a: 2}, {a: 3}] => {a: [1, 2, 3]} 
			cur = { elem[0].tag: map(lambda e: e.values()[0], cur) }

		block[elem.tag] = cur
	else:
		block[elem.tag] = elem.text.strip()
	
	return block


# convert ElementTree Element (root) to json
def xml2json(elem, pretty = True):
	# if the given Element is not the root element, find it
	if hasattr(elem, 'getroot'):
		elem=elem.getroot()

	return json.dumps(elem2list(elem), indent = (4 if pretty else None) )


# convert an xml file to a json file
def xml2json_file(input, output = None, pretty = True, encoding='utf-8'):
	context = et.iterparse(input, events=("start", "end"))
	context = iter(context)
	event, root = context.next()

	json = xml2json(root, pretty)

	# if an output filename is given, write to it, otherwise, return json
	if output != None:
		output = codecs.open(output, "w", encoding)
		output.write(json)
	else:
		return json