"""
    xml2csv.py
    Kailash Nadh, http://nadh.in
    October 2011
    
    License:        MIT License
    Documentation:    http://nadh.in/code/xmlutils.py
"""

import codecs
import xml.etree.ElementTree as et

class xml2csv:

    def __init__(self, input_file, output_file, encoding='utf-8'):
        """Initialize the class with the paths to the input xml file
        and the output csv file

        Keyword arguments:
        input_file -- input xml filename
        output_file -- output csv filename
        encoding -- character encoding
        """

        self.output_buffer = []
        self.output = None

        # open the xml file for iteration
        self.context = et.iterparse(input_file, events=("start", "end"))

        # output file handle
        try:
            self.output = codecs.open(output_file, "w", encoding=encoding)
        except:
            print("Failed to open the output file")
            raise


    def convert(self, tag="item", delimiter=",", ignore=[], noheader=False,
                limit=-1, buffer_size=1000, quotes=True):

        """Convert the XML file to CSV file

            Keyword arguments:
            tag -- the record tag. eg: item
            delimiter -- csv field delimiter
            ignore -- list of tags to ignore
            limit -- maximum number of records to process
            buffer_size -- number of records to keep in buffer before writing to disk
            quotes -- insert quotes around values (e.g. "user@domain.com")

            Returns:
            number of records converted,
        """

        # get to the root
        # to ensure support for python 2/3 versions: iter.next() in python 2 changed to next(iter) in python 3
        try:
            try:
                # for py version 2.x
                event, root = self.context.next()
            except AttributeError:
                # for py version 3.x
                event, root = next(self.context)
        except et.ParseError as e:
            # Invalid XML file - so close the file handle and delete it
            self.output.close()
            os.remove(self.input_file)
            raise e

        items = []
        header_line = []
        field_name = ''
        processed_fields = []

        tagged = False
        started = False
        n = 0


        # iterate through the xml
        for event, elem in self.context:
            # if elem is an unignored child node of the record tag, it should be written to buffer
            should_write = elem.tag != tag and started and elem.tag not in ignore
            # and if a header is required and if there isn't one
            should_tag = not tagged and should_write and not noheader

            if event == 'start':
                if elem.tag==tag:
                    processed_fields=[]
                if elem.tag == tag and not started:
                    started = True
                elif should_tag:
                    # if elem is nested inside a "parent", field name becomes parent_elem
                    field_name = '_'.join((field_name, elem.tag)) if field_name else elem.tag

            else:
                if should_write and elem.tag not in processed_fields:
                    processed_fields.append(elem.tag)
                    if should_tag:
                        header_line.append(field_name)  # add field name to csv header
                        # remove current tag from the tag name chain
                        field_name = field_name.rpartition('_' + elem.tag)[0]
                    items.append('' if elem.text is None else elem.text.strip().replace('"', r'""'))

                # end of traversing the record tag
                elif elem.tag == tag and len(items) > 0:
                    # csv header (element tag names)
                    if header_line and not tagged:
                        self.output.write(delimiter.join(header_line) + '\n')
                    tagged = True

                    # send the csv to buffer
                    if quotes:
                        self.output_buffer.append(r'"' + (r'"' + delimiter + r'"').join(items) + r'"')
                    else:
                        self.output_buffer.append((delimiter).join(items))
                    items = []
                    n += 1

                    # halt if the specified limit has been hit
                    if n == limit:
                        break

                    # flush buffer to disk
                    if len(self.output_buffer) > buffer_size:
                        self._write_buffer()

                elem.clear()  # discard element and recover memory

        self._write_buffer()  # write rest of the buffer to file
        self.output.close()

        return n


    def _write_buffer(self):
        """Write records from buffer to the output file"""

        self.output.write('\n'.join(self.output_buffer) + '\n')
        self.output_buffer = []
