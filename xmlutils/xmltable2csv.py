"""
    xmltable2csv.py
    Yigal Lazarev, http://yig.al
    May 2015
    
    License:        MIT License
    Documentation:    http://nadh.in/code/xmlutils.py
"""

import codecs
import xml.etree.ElementTree as ETree


class xmltable2csv:
    """
    This class is intended to convert tables formatted as XML document, to a
    comma-separated value lines (CSV) file.

    This is a bit different than the xml2csv tool, which tries to convey the XML hierarchy
    into a CSV file - it keeps descending to the selected tags child nodes and translates these as well.

    Example for the expected input to this converter class:
    =======================================================

    A table of the following form:

    Header 1           Header 2
    Value R1C1         Value R1C2
    Value R2C1         Value R2C2

    Will be formatted something along the lines of the following XML in Microsoft Excel:

     <?xml version="1.0" encoding="utf-8"?>
     <?mso-application progid="Excel.Sheet"?>
     <ss:Workbook xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">
     <ss:Table ss:ExpandedColumnCount="11" ss:FullColumns="1" ss:ExpandedRowCount="28" ss:FullRows="1">
      <ss:Row>
        <ss:Cell ss:StyleID="HeaderStyle">
          <ss:Data ss:Type="String">Header 1</ss:Data>
        </ss:Cell>
        <ss:Cell ss:StyleID="HeaderStyle">
          <ss:Data ss:Type="String">Header 2</ss:Data>
        </ss:Cell>
      </ss:Row>
      <ss:Row>
        <ss:Cell>
          <ss:Data ss:Type="String">Value R1C1</ss:Data>
        </ss:Cell>
        <ss:Cell>
          <ss:Data ss:Type="String">Value R1C2</ss:Data>
        </ss:Cell>
      </ss:Row>
      <ss:Row>
        <ss:Cell>
          <ss:Data ss:Type="String">Value R2C1</ss:Data>
        </ss:Cell>
        <ss:Cell>
          <ss:Data ss:Type="String">Value R2C2</ss:Data>
        </ss:Cell>
      </ss:Row>
     </ss:Table>
     </ss:Workbook>

    This might be a bit different in later versions, but the general form is the same. Notice that
    the tags are namespaced, and this namespacing might be somewhat obfuscated, in the form of a xmlns
    property in the containing 'Workbook' tag.

    This class converts simple (not tested with XLSX sheets containing formulas etc) XML-formatted tables
    to csv, regardless of the specific tagging and hierarchy structure.

    Tested with some XLSX files and worked fine even for files that wouldn't convert in tools
    such as dilshod's xlsx2csv.
    """

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
        self.context = ETree.iterparse(input_file, events=("start", "end"))

        # output file handle
        try:
            self.output = codecs.open(output_file, "w", encoding=encoding)
        except:
            print("Failed to open the output file")
            raise

    def convert(self, tag="Data", delimiter=",", noheader=False,
                limit=-1, buffer_size=1000):

        """Convert the XML table file to CSV file

            Keyword arguments:
            tag -- the record tag that contains a single entry's text. eg: Data (Microsoft XLSX)
            delimiter -- csv field delimiter
            limit -- maximum number of records to process
            buffer -- number of records to keep in buffer before writing to disk

            Returns:
            number of records converted
        """

        items = []

        depth = 0
        min_depth = 0
        row_depth = -1
        n = 0

        # iterate through the xml
        for event, elem in self.context:
            if event == "start":
                depth += 1
                continue
            else:
                depth -= 1
                if depth < min_depth:
                    min_depth = depth

            if depth < row_depth and items:
                if noheader:
                    noheader = False
                else:
                    # new line
                    self.output_buffer.append(items)
                items = []
                # flush buffer to disk
                if len(self.output_buffer) > buffer_size:
                    self._write_buffer(delimiter)

            plain_tag = elem.tag
            last_delim = max(elem.tag.rfind('}'), elem.tag.rfind(':'))
            if 0 < last_delim < len(elem.tag) - 1:
                plain_tag = elem.tag[last_delim + 1:]
            if tag == plain_tag:
                if n == 0:
                    min_depth = depth
                elif n == 1:
                    row_depth = min_depth
                n += 1
                if 0 < limit < n:
                    break
                items.append(elem.text)

        self._write_buffer(delimiter)  # write rest of the buffer to file

        return n

    def _write_buffer(self, delimiter):
        """Write records from buffer to the output file"""

        self.output.write('\n'.join([delimiter.join(e) for e in self.output_buffer]) + '\n')
        self.output_buffer = []
