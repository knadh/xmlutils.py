#!/usr/bin/env python

from setuptools import setup

setup(
	name="xmlutils",
	version="1.4",
	description="A set of utilities for processing XML documents and converting to other formats",
	author="Kailash Nadh",
	author_email="kailash.nadh@gmail.com",
	url="http://nadh.in/code/xmlutils.py",
	packages=['xmlutils'],
	download_url="http://github.com/knadh/xmlutils.py",
	license="MIT License",
	entry_points = {
		'console_scripts': [
			'xml2sql = xmlutils.console:run_xml2sql',
			'xml2csv = xmlutils.console:run_xml2csv',
			'xml2json = xmlutils.console:run_xml2json',
			'xmltable2csv = xmlutils.console:run_xmltable2csv'
		],
	},
	classifiers=[
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Programming Language :: Python",
		"Natural Language :: English",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Topic :: Text Processing :: Markup :: XML",
		"Topic :: Software Development :: Libraries"
	]
)
