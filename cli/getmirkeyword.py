#!/usr/bin/python3

import redis
import sys

def factorial(num):
	fact = 1
	for i in range(2,num):
		fact = fact * i
	return fact

def fisher(a, b, c, d):
	return (factorial(a+c)*factorial(b+d)*factorial(a+b)*factorial(c+d))/(factorial(a)*factorial(b)*factorial(c)*factorial(d)*factorial(a+b+c+d))

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

keys = db.keys('*')
allkeynum = len(keys)-1

for key in keycount:
	allkeys = int(db.hget('keywords_count', key).decode())
	f = fisher(keycount[key], allkeys, mirnum - keycount[key], allkeynum - allkeys)
	print(keycount[key], allkeys, mirnum - keycount[key], allkeynum - allkeys, key.decode(), f, sep="\t")
