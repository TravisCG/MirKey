#!/usr/bin/python3

# Put keywords to redis database

import sys
import redis
import re

def createblacklist(filename):
	bl = set()
	f = open(filename, "r")
	for line in f:
		bl.add(line.rstrip())
	f.close()
	return bl

blacklist = createblacklist(sys.argv[2])

f   = open(sys.argv[1], "r")
r   = redis.StrictRedis(host='localhost', db=0)
prg = re.compile("(mir|let|lin|lsy)-*[0-9a-z]+") # yes, we loose bantam
for line in f:
	fields = line.rstrip().split()
	mir = fields[0]
	m = prg.search(mir)
	if m:
		for token in fields[1:]:
			if len(token) < 3: continue # skip 1-2 character
			if token in blacklist:
				print(token, "in blacklist")
				continue # skip common words
			r.sadd(m.group(0), token)
	else:
		print(mir,"skipped")
f.close()
