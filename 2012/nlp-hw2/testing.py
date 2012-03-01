#!/usr/bin/env python

import pprint
import string
import cPickle as pickle
from nltk.corpus import wordnet as wn

#pretty print
pp = pprint.PrettyPrinter(indent=4)

#point to files
testFile = "/home/hr/study/nlp/2012/nlp-hw2/data/eng.testing.bio"
arffFile = "/home/hr/study/nlp/2012/nlp-hw2/data/testing.arff"

#gazetteer data
funcFile = "/home/hr/study/nlp/2012/nlp-hw2/gazetteers/prep.txt"
countriesFile = "/home/hr/study/nlp/2012/nlp-hw2/gazetteers/countries.txt"

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



#strip \n
contents = map(string.strip,contents)
funcs = map(string.strip,funcs)
countries = map(string.strip,countries)

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
	feature.append(str(int(entity[0].lower() in funcs)))

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

	#inNames
	feature.append(str(int(entity[0].title() in names)))

	#inYagoPlaces
	feature.append(str(int(entity[0].title() in places)))

	#class
	feature.append('?')

	features.append(feature)

# strip empty lines and extract features
for line in contents:
	if not line.strip():
		continue
	else:
		entity = line.rstrip().split()
		extractFeature(entity)


with open(arffFile, 'r') as file:
    # read a list of lines into data
    data = file.readlines()

data[9] = '@attribute wnLex {'
for lex in wnset:
	data[9]+=lex+','
data[9] = data[9][:-1] # remove comma
data[9]+='}\n'


with open(arffFile, 'w') as file:
    file.writelines(data)


arff = open(arffFile,"a")

# remove entity word from list of features and join rest by ,
for line in features:
	line.pop(0)
	arff.write((','.join(line))+'\n')

arff.close()
