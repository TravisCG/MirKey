#!/usr/bin/python

import sys

def factorial(num):
        fact = 1
        for i in range(2,num):
                fact = fact * i
        return fact

def fisher(a, b, c, d):
        return (factorial(a+c)*factorial(b+d)*factorial(a+b)*factorial(c+d))/(factorial(a)*factorial(b)*factorial(c)*factorial(d)*factorial(a+b+c+d))

class MirAssoc:
	def __init__(self):
		self.before = dict()
		self.after  = dict()
	def add(self, d, k):
		if k not in d:
			d[k] = 1
		else:
			d[k] += 1
	def addbefore(self, key):
		self.add(self.before, key)
	def addafter(self, key):
		self.add(self.after, key)

# read text file

text = open(sys.argv[1], "r")
mirkey = dict()
for line in text:
	fields = line.rstrip().split()

	if len(fields) > 2:
		if fields[1] not in mirkey:
			mirkey[fields[1]] = MirAssoc()
		mirkey[fields[1]].addafter(fields[2])

	for f in range(2,len(fields)-1):
		if fields[f] not in mirkey:
			mirkey[fields[f]] = MirAssoc()
		mirkey[fields[f]].addbefore(fields[f-1])
		mirkey[fields[f]].addafter(fields[f+1])

	if len(fields) > 2:
		if fields[len(fields)-1] not in mirkey:
			mirkey[fields[len(fields)-1]] = MirAssoc()
		mirkey[fields[len(fields)-1]].addbefore(fields[len(fields)-2])
text.close()

# find associations

allkeysum = 0
for m in mirkey:
	for a in mirkey[m].after:
		allkeysum += mirkey[m].after[a]

for m in mirkey:
	s = 0
	for a in mirkey[m].after:
		s += mirkey[m].after[a]
	for a in mirkey[m].after:
		common = mirkey[m].after[a]
		withoutkeya = s - common
		withoutkeym = 0
		for b in mirkey[a].before:
			if b != m:
				withoutkeym += mirkey[a].before[b]
		nokeyam = allkeysum - common - withoutkeya - withoutkeym
		p = fisher(common,withoutkeym,withoutkeya,nokeyam)
		if p < 0.05:
			print "%s:%s %d %d %d %d" % (m,a,common,withoutkeym,withoutkeya,nokeyam)
