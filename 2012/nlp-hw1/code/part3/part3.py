#!/usr/bin/env python
# @author Hardik Ruparel
# @copyright All Rights Reserved
# @info:1. Parts of Speech tagged in reference to Penn Treebank :
# 		http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

from collections import OrderedDict
from sys import stdout
import pprint

pp = pprint.PrettyPrinter(indent=2)

# Frame Parts-of-Speech list
nounList = ["information","location","instrument","source","destination",\
			"beneficiary","time","location","attribute","experiencer","agent","patient"]
adjList = ["color","age","size","quality"]
advList = ["manner"]

def main():
	
	"""
	Rule definition:
	"S" -> [{"NP":["head","agent"],"VP":["head"]},{"AUX":["head","agent"],"NP":["head","agent"],"VP", ["head"]}]
	"""
	class Grammar:
		def __init__(self,lhs,rhs):
			self.lhs = lhs 	# string, 	eg: "S"
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
		
		elif(rule == "V"): # Verb
			word = frame["type"]
			l = [item for sublist in lexicon[rule] for item in sublist] # flattened list
			for index,w in enumerate(l):
				if(w == word):
					if(inflect["time"]=="present"):
						if(inflect["number"]=="single"):
							return l[index] # Present
						else:
							return l[index+2] # Present & plural
					elif(inflect["time"]=="past"):
						return l[index+1] # Past
					else:
						return "will "+l[index] # Future
		elif(rule == "AUX"): # Auxillary
			word = frame["type"]
			l = [item for sublist in lexicon[rule] for item in sublist] # flattened list
			for index,w in enumerate(l):
				if(w==word):
					if(inflect["time"]=="present"):
						if(inflect["polarity"]=="pos"): 
							return l[index] 			# present positive (can)
						else:
							return l[index+1]			# present negative (cannot)
					else:
						if(inflect["polarity"]=="pos"):
							return l[index+2]			# past positive (could)
						else:
							return l[index+3]			# past negative (could not)
		elif(rule == "ADJ" or rule == "PREP" or rule == "GER"): # Adjective or Preposition or Gerund
			word = frame["type"]
			for index,w in enumerate(lexicon[rule]):
				if(w==word):
					return word
		elif(rule == "TO"):
			return "to"
		
		
	"""Determines Part-of-Speech Type of frame :id
	Eg : posType("agent")
	"""
	def posType(word):
		if word in nounList:
			return "N"
		elif word in verbList:
			return "V"
		elif word in advList:
			return "ADV"

	
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
	# V : [[present, past, future, present-plural, past-pl, future-plural]]
	# AUX : [[present, present-neg, past, past-neg]]
	# ADJ : [list of adj] ,  ADV : [list of adv] , PREP : [list of Prep]
	lexicon = {}

	lexicon = { 
	  "N":[['potato',"potatoes"],["In-N-Out","In-N-Out"],["french-fry","french-fries"],["way","ways"]],\
	  "V": [["cook","cooked","cooks"],["prepare","prepared","prepares"],["use","used","uses"],\
	  		["deliver","delivered","delivers"],["take","took","took"], ["complement","complemented","complements"],\
	  		["is","was","will be"],["do","did","will do"]],
	  "AUX": [["can","cannot","could","could not"],["should","should not","should have","shouldn't have"],\
	   		 ["does","does not","did","did not"],["will","will not","would","would not"]],\
	  "ADJ": ["old","best","new","tasty","fresh","good","whole","trans-fat-free","vegetable","hot"],\
	  "ADV": ["individually","not"],
	  "PREP": ["at","that","we"],
	  "DET": ["a","an","the","that"]
	  "GER": ["regarding"],
	  "TO" : ["to"]
	}

	#pp.pprint(lexicon)
	
	# Test cases
	print findWord("N",{"number":"single"},{"type":"potato"})
	print findWord("V",{"time":"future","number":"plural"},{"type":"prepare"})
	print findWord("AUX",{"time":"past","polarity":"neg"},{"type":"should"})
	print findWord("ADJ",{},{"type":"best"})
	print findWord("PREP",{},{"type":"at"})


if __name__ == '__main__':
	main()