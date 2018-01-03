"""
    xml2json.py
    Kailash Nadh, http://nadh.in
    December 2012
    
    License:        MIT License
    Documentation:    http://nadh.in/code/xmlutils.py
"""

import codecs
import xml.etree.ElementTree as et
import json

class xml2json:

    def __init__(self, input_file, output_file = None, encoding='utf-8'):
        """Initialize the class with the paths to the input xml file
        and the output json file

        Keyword arguments:
        input_file -- input xml filename
        output_file -- output json filename
        encoding -- character encoding
        """

        # open the xml file for iteration
        self.context = et.iterparse(input_file, events=("start", "end"))
        self.output_file = output_file
        self.encoding = encoding

    def get_json(self, pretty=True):
        """
            Convert an XML file to json string (Tested with python 2.7.8 on Windows 7)

            Keyword arguments:
            pretty -- pretty print json (default=True)
        """

        iterator = iter(self.context)

        try:
            while True:
                event, root = iterator.next()
        except StopIteration:
            print("Event StopIteration found, done!")
        finally:
            return self._elem2json(root, pretty)

    def convert(self, pretty=True):
        """
            Convert xml file to a json file

            Keyword arguments:
            pretty -- pretty print json (default=True)
        """

        json = self.get_json(pretty)

        # output file handle
        try:
            output = codecs.open(self.output_file, "w", encoding=self.encoding)
        except:
            print("Failed to open the output file")
            raise

        output.write(json)
        output.close()


    def _elem2list(self, elem):
        """Convert an ElementTree element to a list"""

        block = {}

        # get the element's children
        children = elem.getchildren()

        if children:
            cur = map(self._elem2list, children)

            # create meaningful lists
            scalar = False
            try:
                if elem[0].tag != elem[1].tag:  # [{a: 1}, {b: 2}, {c: 3}] => {a: 1, b: 2, c: 3}
                    cur = dict(zip(
                        map(lambda e: e.keys()[0], cur),
                        map(lambda e: e.values()[0], cur)
                    ))
                else:
                    scalar = True
            except Exception as e:  # [{a: 1}, {a: 2}, {a: 3}] => {a: [1, 2, 3]}
                scalar = True

            if scalar:
                if len(cur) > 1:
                    cur = {elem[0].tag: [e.values()[0] for e in cur if e.values()[0] is not None]}
                else:
                    cur = {elem[0].tag: cur[0].values()[0] }

            block[elem.tag] = cur
        else:
            val = None
            if elem.text:
                val = elem.text.strip()
                val = val if len(val) > 0 else None
            elif elem.attrib:
                val = elem.attrib
                val = val if len(val) > 0 else None

            block[elem.tag] = val 
        
        return block


    def _elem2json(self, elem, pretty=True):
        """
        Convert an ElementTree Element (root) to json
        """
        # if the given Element is not the root element, find it
        if hasattr(elem, 'getroot'):
            elem = elem.getroot()

        return json.dumps(self._elem2list(elem), indent=(4 if pretty else None))
