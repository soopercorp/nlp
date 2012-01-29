#!/usr/bin/env python
# @author Hardik Ruparel
# @copyright All Rights Reserved

from collections import OrderedDict
from sys import stdout
import pprint

pp = pprint.PrettyPrinter(indent=2)

# Frame Parts-of-Speech list
nounList = ["information","location","instrument","source","destination",\
			"beneficiary","time","location","attribute","experiencer","agent","patient"]
verbList = ["color","age","size","quality"]
advList = ["manner"]

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
	
	"""Returns correct word from lexicon
	Eg : findWord("N",{"number":"many"},{"type":"potato"})
			returns "potatoes"
		 findWord("V",{"time":"past"},{"type":"cook"})
		 	returns "cooked"
	"""
	def findWord(rule,inflect,frame):
		if(rule == "N"): # Noun
			word = frame["type"]
			l = [item for sublist in lexicon[rule] for item in sublist] # flattened list
			for index,w in enumerate(l):
				if(w == word):
					if(inflect["number"]=="single"):
						return l[index] # Singular
					else: 
						return l[index+1] # Plural
		
		if(rule == "V"): # Verb
			word = frame["type"]
			l = [item for sublist in lexicon[rule] for item in sublist] # flattened list
			for index,w in enumerate(l):
				if(w == word):
					if(inflect["time"]=="present"):
						return l[index] # Present
					elif(inflect["time"]=="past"):
						return l[index+1] # Past
					else:
						return "will "+l[index] # Future
	

	"""Determines Part-of-Speech Type of frame :id
	Eg : posType(["agent","type"])
	"""
	def posType(word):
		pass
	"""
	Parses the grammar passed with the frame included
	Eg: Parse("NP[head:agent]",frame)
	"""
	def Parse(grammar,frame):
		pass
	# initialize list of grammar rules
	g = []
	
	# add items
	rhsRule = 	[OrderedDict([("NP",["head","agent"]),("VP",["head"])]),\
				OrderedDict([("AUX",["head","agent"]),("NP",["head","agent"]),("VP",["head"])]),\
				OrderedDict([("DET",["head","determiner"]),("ADJ*",["head"]),("N",["head","type"]),("PP*",["head"])])]
	
	# add rules for S
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

	# lexicon format
	# N : [[singular,plural]]
	# V : [[present, past, future]]
	# AUX : [[present, present-neg, past, past-neg]]
	# ADJ : [list of adj] ,  ADV : [list of adv] , PREP : [list of Prep]
	lexicon = {}

	lexicon = { 
	  "N":[['potato',"potatoes"],["In-N-Out","In-N-Out"],["french-fry","french-fries"]],\
	  "V": [["cook","cooked"],["prepare","prepared"],["use","used"],["deliver","delivered"],["take","took"]],\
	  "AUX": [["can","cannot","could","could not"],["should","shouldn't","should have","shouldn't have"],\
	   		 ["does","doesn't","did","didn't"],["will","won't","would","wouldn't"]],\
	  "ADJ": ["old","new","tasty","fresh","good","whole","trans-fat-free","vegetable","hot"],\
	  "ADV": ["individually"],
	  "PREP": ["at","that"]
	}

	#pp.pprint(lexicon)
	
	# Test cases
	print findWord("N",{"number":"single"},{"type":"potato"})
	print findWord("V",{"time":"past"},{"type":"prepare"})


if __name__ == '__main__':
	main()