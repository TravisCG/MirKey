#!/usr/bin/python3

import sys
import re

# Function to remove unwanted characters
def filterstr(instr):
	nohtml   = re.sub("<[^>]+>", " ", instr)     # no html tags
	nocode   = re.sub("&#\d+;"," ", nohtml)      # no stupid codes
	nonum    = re.sub(" \d{1,3} ", " ", nocode)  # no individual numbers
	nobrac   = re.sub(' [.[:^()·]+ '," ",nonum)  # no stupid characters
	nobrac   = re.sub("]"," ",nobrac)
	nobrac   = re.sub(","," ",nobrac)
	nobrac   = re.sub('"'," ",nobrac)
	onespace = re.sub("\s+"," ",nobrac)          # more than one whitespace collapsed to one
	nostnum  = re.sub("^\d+ ","",onespace)       # no heading number
	return nostnum.lower()

# remove tokens found more than onece
def unique(instr):
	tokens = instr.split(" ")
	uni = dict()
	for i in tokens: uni[i] = 1
	return tokens[0] + " " + " ".join(uni.keys())

# main part
wiki = open(sys.argv[1],"r")
longline = ""
for line in wiki:
	if line.endswith("\\\n"):
		longline += line.rstrip("\\\n") + " "
	else:
		longline += line + " "
		longline = filterstr(longline)
		longline = unique(longline)
		print(longline)
		longline = ""
wiki.close()
