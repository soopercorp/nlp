#!/usr/bin/env python

import re
import pprint
import string

pp = pprint.PrettyPrinter(indent=4)

testFile = "/home/hr/study/nlp/2012/nlp-hw2/eng.train.bio"
funcFile = "/home/hr/study/nlp/2012/nlp-hw2/prep.txt"
arffFile = "/home/hr/study/nlp/2012/nlp-hw2/features.arff"

puncs = ['.',',','!','(',')','-',':',';','~','--','"','?','$',"''"]

#open testfile
fd = open(testFile)
contents = fd.readlines()
fd.close()

#open functional word file
funcFd = open(funcFile)
funcs = funcFd.readlines()
funcFd.close()

#strip \n
contents = map(string.strip,contents)
funcs = map(string.strip,funcs)

# features
# [posTag,isAllCaps,firstLetterCaps,wordLength,isFuncWord,isPunctuation
# contatinsDots, ]

features = []

def extractFeature(entity):
	feature = []

	feature.append(entity[0])
	#posTag
	if entity[1] not in puncs:
		feature.append(entity[1])
	else:
		feature.append('?')

	#allCaps
	if entity[0].isupper():
		feature.append('1')
	else:
		feature.append('0')	

	#firstCaps
	if(entity[0][0].isupper()):
		feature.append('1')
	else:
		feature.append('0')

	#word length
	feature.append(str(len(entity[0])))

	#functional word = determiner,conjunction,preposition
	feature.append(str(int(entity[0] in funcs)))

	#punctuation mark
	feature.append(str(int(entity[0] in puncs)))

	#contains dots
	if(entity[0] != '.'):
		feature.append(str(int('.' in entity[0])))
	else:
		feature.append('0')

	#class
	feature.append(entity[2])

	features.append(feature)

for line in contents:
	if not line.strip():
		continue
	else:
		entity = line.rstrip().split()
		extractFeature(entity)

arff = open(arffFile,"a")

# remove entity word from list of features and join rest by ,
for line in features:
	line.pop(0)
	arff.write((','.join(line))+'\n')

arff.close()
