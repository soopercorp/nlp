#!/usr/bin/env python
# @author Hardik Ruparel
# @copyright All Rights Reserved

from collections import OrderedDict

def main():
	
	"""
	Rule definition:
	"S" -> {"NP":["head","agent"],"VP":["head"]}
	"""
	class Grammar:
		def __init__(self,lhs,rhs):
			self.lhs = lhs 	# string, 		eg: "S"
			self.rhs = rhs 	# list of ordereddict,	eg: [{"NP":["head","agent"],"VP":["head"]},
							#  {"AUX":}
		
		def parse(self):
			print self.lhs
			for i,rule in enumerate(self.rhs):
				print "Rule {0}: ".format(i)
				for k,v in rule.items():
					print k,v
		

	# grammar list
	g = []
	
	# add items
	rhsRule = \
	[OrderedDict([("NP",["head","agent"]),("VP",["head"])]),\
	OrderedDict([("AUX",["head","agent"]),("NP",["head","agent"]),("VP",["head"])])]
	
	g.append(Grammar("S",rhsRule))
	
	# loop over grammar and print rules
	for i in range(len(g)):
		Grammar.parse(g[i])
	
if __name__ == '__main__':
	main()