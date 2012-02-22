#!/usr/bin/env python

import re

file = "/home/hr/Desktop/kozareva-assignment-2/eng.train.bio"

fd = open(file)
contents = fd.readlines()
fd.close()

def org(entity):
	if(entity[2]!= "O"):
		if(entity[2].split("-")[1] == "ORG"):
			return 1
		else:
			return 0

def extractFeature(entity):
	if(org(entity)):
		pass
		print entity[0] + " is " + entity[2]

for line in contents:
	if not line.strip():
		continue
	else:
		entity = line.rstrip().split()
		if entity[0] == "." or entity[0] == ",":
			continue
		else:
			extractFeature(entity)