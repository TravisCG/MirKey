#!/usr/bin/python3

import sys
import re

class MIR:
	""" Class to store mirbase fields """
	def __init__(self):
		self.pmid = list();
		self.text = ""
		self.mirid = ""
	def simplify(self):
		self.text = self.text.lower()
		self.text = re.sub('[.,:;"]+'," ",self.text)
		self.text = re.sub('\[', " ",self.text)
		self.text = re.sub('\]', " ",self.text)
		self.text = re.sub(' mir\S+', ' ', self.text)
		self.text = re.sub(' \d+ ', ' ', self.text)
		self.text = re.sub("\s+"," ",self.text)

# read abstract file
abstract = dict()
f = open(sys.argv[2],"r")
for line in f:
	fields = line.rstrip().split()
	abstract[fields[0]] = " ".join(fields[1:])
f.close()

store = dict()

# read mir.dat file
f = open(sys.argv[1], "r")
for line in f:
	if line.startswith("ID"):
		mir = MIR()
		key = line.split()[1].lower()
		mir.mirid = key
	if line.startswith("RX"):
		mir.pmid.append(line.split()[2].rstrip("."))
	if line.startswith("CC"):
		mir.text += line.lstrip("CC   ")
	if line.startswith("DE"):
		mir.text += line.lstrip("DE   ")
	if line.startswith("//"):
#		mir.simplify()
		store[key] = mir
f.close()

# write out results
for k in store.keys():
	abstr = ""
	for l in store[k].pmid:
		abstr += abstract[l]
	store[k].text += " " + abstr
	store[k].simplify()
	print(store[k].mirid, store[k].text)
