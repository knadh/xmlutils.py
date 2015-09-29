"""
	xml2sql.py
	Kailash Nadh, http://nadh.in
	October 2011
	
	License:        MIT License
	Documentation:    http://nadh.in/code/xmlutils.py
"""

import codecs
import xml.etree.ElementTree as et

class xml2sql:

	def __init__(self, input_file, output_file, encoding='utf-8'):
		"""Initialize the class with the paths to the input xml file
		and the output sql file

		Keyword arguments:
		input_file -- input xml filename
		output_file -- output sql filename
		encoding -- character encoding
		"""

		self.output_buffer = []
		self.sql_insert = None
		self.output = None
		self.num_insert = 0

		# open the xml file for iteration
		self.context = et.iterparse(input_file, events=("start", "end"))

		# output file handle
		try:
			self.output = codecs.open(output_file, "w", encoding=encoding)
		except:
			print("Failed to open the output file")
			raise


	def convert(self, tag="item", table="table", ignore=[], limit=-1, packet=8):
		"""Convert the XML file to SQL file

		 	Keyword arguments:
			tag -- the record tag. eg: item
			table -- table name
			ignore -- list of tags to ignore
			limit -- maximum number of records to process
			packet -- maximum size of an insert query in MB (MySQL's max_allowed_packet)

			Returns:
			{	num: number of records converted,
				num_insert: number of sql insert statements generated
			}
		"""

		self.context = iter(self.context)

		# get to the root
		event, root = self.context.next()

		items = []
		fields = []
		field_name = ''

		tagged = False
		started = False

		sql_len = 0
		n = 0

		packet_size = 0
		max_packet = 1048576 * packet


		# iterate through the xml
		for event, elem in self.context:
			# if elem is an unignored child node of the record tag, it should be written to buffer
			should_write = elem.tag != tag and started and elem.tag not in ignore
			# and other fields that haven't been created
			should_tag = not tagged and should_write

			if event == 'start':
				if elem.tag == tag and not started:
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
				elif elem.tag == tag and len(items) > 0:
					tagged = True

					if self.sql_insert is None:
						self.sql_insert = 'INSERT INTO ' + table + ' (' + ','.join(fields) + ')\n'

					sql = r'("' + r'", "'.join(items) + r'")'
					sql_len += len(sql)

					if sql_len + len(self.sql_insert) + 100 < max_packet:
						# store the sql statement in the buffer
						self.output_buffer.append(sql)
					else:
						# packet size exceeded. flush the sql and start a new insert query
						self._write_buffer()
						self.output_buffer.append(sql)
						sql_len = 0

					items = []
					n += 1

					# halt if the specified limit has been hit
					if n == limit:
						break

				elem.clear()  # discard element and recover memory

		self._write_buffer()  # write rest of the buffer to file

		return {"num": n, "num_insert": self.num_insert}


	def _write_buffer(self):
		"""Write records from buffer to the output file"""

		self.output.write(self.sql_insert + 'VALUES\n' + ', \n'.join(self.output_buffer) + ';\n\n')
		self.output_buffer = []
		self.num_insert += 1
