"""
    xml2json.py
    Kailash Nadh, http://nadh.in
    December 2012
    
    License:        MIT License
    Documentation:    http://nadh.in/code/xmlutils.py
"""

import codecs
import lxml.etree as et
import json


def elem2list(elem):
    """
    Convert an ElementTree element to a list
    """
    block = {}

    # get the element's children
    children = elem.getchildren()

    if children:
        cur = map(elem2list, children)

        # create meaningful lists
        if elem[0].tag != elem[1].tag:  # [{a: 1}, {b: 2}, {c: 3}] => {a: 1, b: 2, c: 3}
            cur = dict(zip(
                map(lambda e: e.keys()[0], cur),
                map(lambda e: e.values()[0], cur)
            ))
        else:  # [{a: 1}, {a: 2}, {a: 3}] => {a: [1, 2, 3]}
            cur = {elem[0].tag: [e.values()[0] for e in cur]}

        block[elem.tag] = cur
    else:
        block[elem.tag] = elem.text.strip()
    
    return block


def xml2json(elem, pretty=True):
    """
    Convert an ElementTree Element (root) to json
    """
    # if the given Element is not the root element, find it
    if hasattr(elem, 'getroot'):
        elem = elem.getroot()

    return json.dumps(elem2list(elem), indent=(4 if pretty else None))


def xml2json_file(input_file, output=None, pretty=True, encoding='utf-8'):
    """
    Convert xml file to json
    """
    context = et.iterparse(input_file, events=("start", "end"))
    context = iter(context)
    event, root = context.next()

    json = xml2json(root, pretty)

    # if an output filename is given, write to it, otherwise, return json
    if output is not None:
        output = codecs.open(output, "w", encoding)
        output.write(json)
    else:
        return json