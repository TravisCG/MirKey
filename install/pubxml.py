#!/usr/bin/python

"""
This script extract abstract title and text from PubMed's XML file
generating by getabstract.sh

The output is one line lower case text.
"""

import sys
from xml.dom.minidom import parse, parseString

xmlstr = ""
for line in sys.stdin:
	xmlstr += line.rstrip() + " "

xml    = parseString(xmlstr)
subxml = xml.getElementsByTagName('pre')[0].firstChild.nodeValue
xml    = parseString(subxml.encode('ascii', 'xmlcharrefreplace'))
output = ""

# read title
for title in xml.getElementsByTagName('ArticleTitle'):
	output += title.firstChild.nodeValue.lower() + " "

# read abstract text
for text in xml.getElementsByTagName('AbstractText'):
	output += text.firstChild.nodeValue.lower() + " "

try:
	print output
except UnicodeEncodeError:
	print output.encode('ascii','ignore')
