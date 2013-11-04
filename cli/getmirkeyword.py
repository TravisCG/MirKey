#!/usr/bin/python3

import redis
import sys

def printHelp():
	txt = """
	Small RNA Keyword retreival
	Usage:
	./getmirkeyword.py -file mylist.txt
	Arguments
	-host: host of the Redis database (default: localhost)
	-db: Redis db number (default: 0)
	-file: input file
	-h this help
	"""
	print(txt)
	sys.exit(0)

host     = 'localhost'
dbnum    = 0
filename = ''

if len(sys.argv) < 3:
	printHelp()

for i in range(1, len(sys.argv)):
	if sys.argv[i] == '-host': host = sys.argv[i+1]
	if sys.argv[i] == '-db': dbnum = int(sys.argv[i+1])
	if sys.argv[i] == '-file': filename = sys.argv[i+1]
	if sys.argv[i] == '-h': printHelp()

db = redis.StrictRedis(host=host, db=dbnum)

mirlist = open(filename,"r")
keycount = dict()
mirnum = 0
for line in mirlist:
	mirid = line.rstrip().lower()
	keywords = db.smembers(mirid)
	if len(keywords) == 0:
		print("This ID not found in DB",mirid, file=sys.stderr)
		continue
	for key in keywords:
		if key in keycount:
			keycount[key] += 1
		else:
			keycount[key] = 1
	mirnum += 1
mirlist.close()

# dirty hack later put it to db
keys = db.keys('*')
allkeynum = len(keys)
allkeys = dict()
for i in keys:
	for kw in db.smembers(i):
		if kw in allkeys:
			allkeys[kw] += 1
		else:
			allkeys[kw] = 1

for key in keycount:
	print(keycount[key], allkeys[key], mirnum - keycount[key], allkeynum - allkeys[key], key.decode(),sep="\t")
