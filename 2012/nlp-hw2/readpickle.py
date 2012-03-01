import cPickle as pickle

pkl_file = open('/home/hr/study/nlp/2012/nlp-hw2/hasFamilyName.pkl', 'rb')

names = pickle.load(pkl_file)

print 'Ayn' in names

pkl_file.close()
