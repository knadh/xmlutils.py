> **NOTICE (May 2017):** I'm no longer able to maintain this project or look at posted issues.
If you're interested in maintaining, please let me know.

# xmlutils.py

xmlutils.py is a set of Python utilities for processing xml files serially  
for converting them to various formats (SQL, CSV, JSON). The scripts use 
ElementTree.iterparse() to iterate through nodes in an XML document, thus not 
needing to load the entire DOM into memory. The scripts can be used to churn 
through large XML files (albeit taking long :P) without memory hiccups.

Simple table-representing XMLs can be converted to CSV using xmltable2csv. It assumes each entry is encapsulated
in some tag, and successfuly tested on some XLSX files.

Blind conversion of XML to CSV and SQL is not recommended.
It only works if the structure of the XML document is simple (flat). 
On the other hand, xml2json supports complex XML documents with multiple
nested hierarchies. Lastly, the XML files are not validated at the time of conversion.


- Kailash Nadh, June 2013
- Yigal Lazarev, May 2015
- License: MIT License
- Documentation: [http://nadh.in/code/xmlutils.py](http://nadh.in/code/xmlutils.py)
- Pypi: [https://pypi.python.org/pypi/xmlutils](https://pypi.python.org/pypi/xmlutils)


#Installation
With pip or easy_install

```pip install xmlutils``` or ```easy_install xmlutils```

Or from the source

```python setup.py install```

#Commandline utilities
Once the package is installed, the three bundled commandline utilities should be available
from the terminal.

##xml2csv
Convert an XML document to a CSV file.

```
xml2csv --input "samples/fruits.xml" --output "samples/fruits.csv" --tag "item"
```

######Arguments
```
--input 	Input XML document's filename*
--output 	Output CSV file's filename*
--tag 		The tag of the node that represents a single record (Eg: item, record)*
--delimiter 	Delimiter for seperating items in a row. Default is , (a comma followed by a space)
--ignore 	A space separated list of element tags in the XML document to ignore
--noheader 	Exclude CSV fields header (first line). Off by default
--encoding 	Character encoding of the document. Default is utf-8
--limit 	Limit the number of records to be processed from the document to a particular number. Default is no limit (-1)
--buffer 	The number of records to be kept in memory before it is written to the output CSV file. Helps reduce the number of disk writes. Default is 1000
```

##xmltable2csv
Convert an XML table to a CSV file.

```
xmltable2csv --input "samples/fruits.xml" --output "samples/fruits.csv" --tag "Data"
```

######Arguments
```
--input         Input XML table's filename*
--output        Output CSV file's filename*
--tag           The tag of the node that represents a single record (Eg: Data, record)*
--delimiter     Delimiter for seperating items in a row. Default is , (a comma followed by a space)
--header        Whether to print the header (first row of records in the XML) in the first line; 1=yes, 0=no. Default is 1.
--encoding      Character encoding of the document. Default is utf-8
--limit         Limit the number of records to be processed from the document to a particular number. Default is no limit (-1)
--buffer        The number of records to be kept in memory before it is written to the output CSV file. Helps reduce the number of disk writes. Default is 1000.
```

##xml2sql
Convert an XML document to an SQL file.

```
xml2sql --input "samples/fruits.xml" --output "samples/fruits.sql" --tag "item" --table "myfruits"
```

######Arguments
```
--tag           the record tag. eg: item
--table         table name
--ignore        list of tags to ignore
--limit         maximum number of records to process
--packet        maximum size of an insert query in MB (MySQL's max_allowed_packet)
```

##xml2json
Convert XML to JSON.
xml2json supports hierarchies nested to any number of levels.

```xml2json --input "samples/fruits.xml" --output "samples/fruits.json"```

#Modules

##xmlutils.xml2sql
```python
from xmlutils.xml2sql import xml2sql

converter = xml2sql("samples/fruits.xml", "samples/fruits.sql", encoding="utf-8")
converter.convert(tag="item", table="table")
```

######Arguments
```
tag 	-- the record tag. eg: item
table	-- table name
ignore	-- list of tags to ignore
limit	-- maximum number of records to process
packet	-- maximum size of an insert query in MB (MySQL's max_allowed_packet)

Returns:
{	num: number of records converted,
	num_insert: number of sql insert statements generated
}
```

##xmlutils.xml2csv
```python
from xmlutils.xml2csv import xml2csv

converter = xml2csv("samples/fruits.xml", "samples/fruits.csv", encoding="utf-8")
converter.convert(tag="item")
```

######Arguments
```
tag	-- the record tag. eg: item
delimiter -- csv field delimiter
ignore	-- list of tags to ignore
limit	-- maximum number of records to process
buffer	-- number of records to keep in buffer before writing to disk

Returns:
number of records converted
```

##xmlutils.xml2json
```python
from xmlutils.xml2json import xml2json

converter = xml2json("samples/fruits.xml", "samples/fruits.json", encoding="utf-8")
converter.convert()

# to get a json string
converter = xml2json("samples/fruits.xml", encoding="utf-8")
print converter.get_json()
```

######Arguments
```
pretty	-- pretty print?
```
