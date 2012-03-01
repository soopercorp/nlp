import cPickle as pickle

testFile = "/home/hr/study/nlp/2012/nlp-hw2/data/try.bio"
arffFile = "/home/hr/study/nlp/2012/nlp-hw2/data/try.arff"

#gazetteer data
funcFile = "/home/hr/study/nlp/2012/nlp-hw2/gazetteers/prep.txt"
countriesFile = "/home/hr/study/nlp/2012/nlp-hw2/gazetteers/countries.txt"


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

out = open('test.pkl','wb')

pickle.dump(contents, out)

out.close()

out = open("funcs.pkl",'wb')

pickle.dump(funcs, out)

out.close()

out = open("countries.pkl",'wb')

pickle.dump(countries, out)

out.close()
