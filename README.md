# xmlutils.py
A set of Python scripts for processing xml files serially, 
namely converting them to other formats (SQL, CSV, JSON). The scripts use ElementTree.iterparse() 
to iterate through nodes in an XML file, thus not needing to load the whole DOM into memory. 
The scripts can be used to churn through large XML files (albeit taking long :P) without 
memory hiccups. (Note: The XML files are NOT validated by the scripts.)

Kailash Nadh, October 2011

License:	MIT License

Documentation: http://kailashnadh.name/code/xmlutils.py

## xml2csv.py
Convert an XML document to a CSV file.

<pre>
python xml2csv.py --input "samples/fruits.xml" --output "samples/fruits.csv" --tag "item"
</pre>

### options
<table>
	<tbody>
		<tr>
			<td>--input</td>
			<td>
				Input XML document's filename*
			</td>
		</tr>
		<tr>
			<td>--output</td>
			<td>
				Output CSV file's filename*
			</td>
		</tr>
		<tr>
			<td>--tag</td>
			<td>
				The tag of the node that represents a single record (Eg: item, record)*
			</td>
		</tr>
		<tr>
			<td>--delimiter</td>
			<td>
				Delimiter for seperating items in a row. Default is , (a comma followed by a space)
			</td>
		</tr>
		<tr>
			<td>--ignore</td>
			<td>
				A space separated list of element tags in the XML document to ignore.
			</td>
		</tr>
		<tr>
			<td>--header</td>
			<td>
				Whether to print the CSV header (list of fields) in the first line; 1=yes, 0=no. Default is 1.
			</td>
		</tr>
		<tr>
			<td>--encoding</td>
			<td>
				Character encoding of the document. Default is utf-8
			</td>
		</tr>
		<tr>
			<td>--limit</td>
			<td>
				Limit the number of records to be processed from the document to a particular number. 
				Default is no limit (-1)
			</td>
		</tr>
		<tr>
			<td>--buffer</td>
			<td>
				The number of records to be kept in memory before it is written to the output CSV file. Helps 
				reduce the number of disk writes. Default is 1000.
			</td>
		</tr>
	</tbody>
</table>

##xml2sql.py
Convert an XML document to an SQL file.

<pre>
python xml2sql.py --input "samples/fruits.xml" --output "samples/fruits.sql" --tag "item" --table "myfruits"
</pre>

### options
<table>
	<tbody>
		<tr>
			<td>--input</td>
			<td>
				Input XML document's filename*
			</td>
		</tr>
		<tr>
			<td>--output</td>
			<td>
				Output SQL file's filename*
			</td>
		</tr>
		<tr>
			<td>--tag</td>
			<td>
				The tag of the node that represents a single record (Eg: item, record)*
			</td>
		</tr>
		<tr>
			<td>--ignore</td>
			<td>
				A space separated list of element tags in the XML document to ignore.
			</td>
		</tr>
		<tr>
			<td>--encoding</td>
			<td>
				Character encoding of the document. Default is utf-8
			</td>
		</tr>
		<tr>
			<td>--limit</td>
			<td>
				Limit the number of records to be processed from the document to a particular number. 
				Default is no limit (-1)
			</td>
		</tr>
		<tr>
			<td>--packet</td>
			<td>
				Maximum size of a single INSERT query in MBs. Default is 8. Set based on MySQL's 
				max_allowed_packet configuration.
			</td>
		</tr>
	</tbody>
</table>

##xml2json.py
Convert XML to JSON.

Unlike xml2sql and xml2csv, xml2py is not a stand alone utility, but a library. Moreover, it
supports hierarchies nested to any number of levels.

### usage
```python
from xml2json import *

# given an ElementTree Element, return its json
json = xml2json(elem)


# __________ Working with files
# xml2json_file(input_filename, output_filename[optional], prettyprint[True or False], file_encoding[default: utf-8])

# read an xml file and return json
json = xml2json_file("samples/fruits.xml")

# read an xml file and write json to a file
xml2json_file("samples/fruits.xml", "samples/fruits.json")
```