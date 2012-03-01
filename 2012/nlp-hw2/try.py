import re
import cPickle as pickle
import string

yNameFile = "/home/hr/study/nlp/2012/nlp-hw2/gazetteers/hasPopulation.tsv"

fd = open(yNameFile)
yNames = fd.readlines()
fd.close()

output = open('hasPopulation.pkl', 'wb')

yNames = map(string.strip,yNames)

ls = set()

for i in range(len(yNames)):

	yNames[i] = re.sub("[\\u]*#*[0-9]+","",yNames[i])
	yNames[i] = re.sub("\\\\","",yNames[i])
	yNames[i] = re.sub("c_",", ",yNames[i])

	yNames[i] = re.sub("town|village|city|state","",yNames[i])
	yNames[i] = re.sub("_,",",",yNames[i])
	yNames[i] = re.sub("_"," ",yNames[i])
	
	yNames[i] = yNames[i].strip('\s\t')

	for loc in yNames[i].split(','):
		ls.add(loc)

yNames = frozenset(ls)

pickle.dump(yNames,output)

output.close()

print 'kolkata'.title() in yNames

