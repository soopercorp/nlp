import sys

testFile = sys.argv[1]

#open testfile
fd = open(testFile)
contents = fd.readlines()
fd.close()

for line in contents:
	entity = line.rstrip().split()
	if entity:
		if entity[1] == sys.argv[2]:
			print entity
