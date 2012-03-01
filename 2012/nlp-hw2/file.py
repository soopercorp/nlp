#!/usr/bin/env python

import pprint
import string
import cPickle as pickle
import sys
from nltk.corpus import wordnet as wn


#pretty print
pp = pprint.PrettyPrinter(indent=4)

#point to files
testFile = sys.argv[1]
arffFile = sys.argv[2]

#gazetteer data
funcFile = "/home/hr/study/nlp/2012/nlp-hw2/gazetteers/prep.txt"
countriesFile = "/home/hr/study/nlp/2012/nlp-hw2/gazetteers/countries.txt"
datesFile = "/home/hr/study/nlp/2012/nlp-hw2/gazetteers/dates.txt"

pkl_file = open('/home/hr/study/nlp/2012/nlp-hw2/hasFamilyName.pkl', 'rb')
names = pickle.load(pkl_file)
pkl_file.close()

places_file = open('/home/hr/study/nlp/2012/nlp-hw2/hasPopulation.pkl', 'rb')
places = pickle.load(places_file)
places_file.close()

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
fd = open(countriesFile)
countries = fd.readlines()
fd.close()

#dates file
fd = open(datesFile)
dates = fd.readlines()
fd.close()

#strip \n
contents = map(string.strip,contents)
funcs = map(string.strip,funcs)
countries = map(string.strip,countries)
dates = map(string.strip,dates)

# features
# [posTag,isAllCaps,firstLetterCaps,wordLength,isFuncWord,isPunctuation
# contatinsDots, ]

features = []
wnset = set()

def extractFeature(entity):
	if not entity:
		return

	feature = []

	#posTag
	if entity[1] not in puncs:
		feature.append(entity[1])
	else:
		feature.append('punc')

	#isInitial
	feature.append(str(int((len(entity[0]) == 2 and '.' in entity[0]))))
		
	#functional word = determiner,conjunction,preposition
	feature.append(str(int(entity[0].lower() in funcs)))
	
	#allCaps - not considering func words
	if entity[0].isupper() and feature[-1] == '0':
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

	#punctuation mark
	feature.append(str(int(entity[0] in puncs)))

	#contains dots
	if(entity[0] != '.'):
		feature.append(str(int('.' in entity[0])))
	else:
		feature.append('0')

	#wordnet lexical info
	wnres = wn.synsets(entity[0])
	if wnres and ("person" in wnres[0].lexname or "location" in wnres[0].lexname):
		feature.append(wnres[0].lexname)
		wnset.add(wnres[0].lexname)
	else:
		feature.append('?')

	#isCountry
	feature.append(str(int(entity[0].title() in countries)))

	#inYagoNames
	feature.append(str(int(entity[0].title() in names)))

	#inYagoPlaces
	feature.append(str(int(entity[0].title() in places)))

	#isDate
	if entity[0].title() in dates:
		feature.append('1')
		feature[0] = "date"
	else:
		feature.append('0')
	
	"""
	placeDone = 0
	for place in places:
		if(lev.ratio(entity[0].lower(),place.lower()) > 0.9):
			feature.append('1')
			placeDone = 1
	if not placeDone:
		feature.append('0')
	"""

	#prevPOSTag
	if features:
		feature.append(features[-1][0])
	else:
		feature.append('?')

	#class
	feature.append(entity[2])

	features.append(feature)


# strip empty lines and extract features
for line in contents:
	entity = line.rstrip().split()
	extractFeature(entity)

# write wordNet @attribute line
with open(arffFile, 'r') as file:
    # read a list of lines into data
    data = file.readlines()

data[10] = '@attribute wnLex {'
for lex in wnset:
	data[10]+=lex+','
data[10] = data[10][:-1] # remove comma
data[10]+='}\n'

with open(arffFile, 'w') as file:
    file.writelines(data)

arff = open(arffFile,"a")

# join and write to file
for line in features:
	arff.write((','.join(line))+'\n')

arff.close()
