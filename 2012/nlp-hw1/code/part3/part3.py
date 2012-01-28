#!/usr/bin/env python
# @author Hardik Ruparel
# @copyright All Rights Reserved

from collections import OrderedDict
from sys import stdout
import pprint

pp = pprint.PrettyPrinter(indent=2)

def main():
	
	"""
	Rule definition:
	"S" -> [{"NP":["head","agent"],"VP":["head"]},{"AUX":["head","agent"],"NP":["head","agent"],"VP", ["head"]}]
	"""
	class Grammar:
		def __init__(self,lhs,rhs):
			self.lhs = lhs 	# string, 		eg: "S"
			self.rhs = rhs 	# list of ordereddict,	eg: [{"NP":["head","agent"],"VP":["head"]},
							#  {"AUX":["head","agent"],"NP":["head","agent"],"VP", ["head"]}]
		
		def parse(self):
			for i,rule in enumerate(self.rhs):
				print "Rule {0}: ".format(i+1)
				print self.lhs+": ",
				for k,v in rule.items():
					stdout.write(k)
					print " {0} ".format(v),
				print "\n"
		
		
	# grammar list
	g = []
	
	# add items
	rhsRule = \
	[OrderedDict([("NP",["head","agent"]),("VP",["head"])]),\
	OrderedDict([("AUX",["head","agent"]),("NP",["head","agent"]),("VP",["head"])]),\
	OrderedDict([("DET",["head","determiner"]),("ADJ*",["head"]),("N",["head","type"]),("PP*",["head"])])]
	
	# add S
	g.append(Grammar("S",rhsRule)) 

	# loop over grammar and print rules
	for i in range(len(g)):
		Grammar.parse(g[i])
	
	# Initialize frame
	frame = {}

	inRep = [("type","eat"),("agent",dict((["type","man"],["size","large"]))),\
			("pateint",dict((["type","peach"],["size","small"],["color","red"]))),\
			("time","past"),("speechact","question"),("polarity","pos")]
	frame = dict(inRep)

	pp.pprint(frame)
		
if __name__ == '__main__':
	main()