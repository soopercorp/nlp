#!/usr/bin/env python

import pprint
import string
from nltk.corpus import wordnet as wn 

#pretty print
pp = pprint.PrettyPrinter(indent=4)

#point to files
testFile = "/home/hr/study/nlp/2012/nlp-hw2/data/try.bio"
arffFile = "/home/hr/study/nlp/2012/nlp-hw2/data/try.arff"

#gazetteer data
funcFile = "/home/hr/study/nlp/2012/nlp-hw2/gazetteers/prep.txt"
countriesFile = "/home/hr/study/nlp/2012/nlp-hw2/gazetteers/countries.txt"

#punctuations
puncs = ['.',',','!','(',')','-',':',';','~','--','"','?','$',"''"]

#open testfile
fd = open(testFile)
contents = fd.readlines()
fd.close()

#open functional word file
fd = open(funcFile)
funcs = fd.readlines()
fd.close()

#countries file

#strip \n
contents = map(string.strip,contents)
funcs = map(string.strip,funcs)

# features
# [posTag,isAllCaps,firstLetterCaps,wordLength,isFuncWord,isPunctuation
# contatinsDots, ]

features = []
wnset = set()

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

	#wordnet lexical info
	wnres = wn.synsets(entity[0])
	if wnres:
		feature.append(wnres[0].lexname)
		wnset.add(wnres[0].lexname)
	else:
		feature.append('?')

	#class
	feature.append(entity[2])

	features.append(feature)

for line in contents:
	if not line.strip():
		continue
	else:
		entity = line.rstrip().split()
		extractFeature(entity)

# need to write wnset
# @attribte wnLex {verb.social,verb.stative}

"""
with open(arffFile, 'r') as file:
    # read a list of lines into data
    data = file.readlines()

data[9] = '@attribute wnLex {'
for lex in wnset:
	data[9]+=lex+','
data[9] = data[9][:-1]
data[9]+='}\n'


with open(arffFile, 'w') as file:
    file.writelines(data)


arff = open(arffFile,"a")

# remove entity word from list of features and join rest by ,
for line in features:
	line.pop(0)
	arff.write((','.join(line))+'\n')

arff.close()

"""