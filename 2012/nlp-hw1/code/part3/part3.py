#!/usr/bin/env python
# @author Hardik Ruparel
# @copyright All Rights Reserved
# @info:1. Parts of Speech tagged in reference to Penn Treebank :
# 		http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

from collections import OrderedDict
from sys import stdout
import pprint
import random

pp = pprint.PrettyPrinter(indent=2)

# frame Parts-of-Speech list
nounList = ["information","location","instrument","source","destination",\
			"beneficiary","time","location","attribute","experiencer","agent","patient"]
adjList = ["color","age","size","quality"]
advList = ["manner"]

agentNum = "" 	# Agent is singular or plural
patientNum = ""	# Patient is singular or plural

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
							if(inflect["polarity"] == "pos"):
								return l[index] # Present (Eat)
							else:
								# have to find an aux
								ls = [item for sublist in lexicon["AUX"] for item in sublist] # flattened list
								sel = [] # will select randomly from this list
								for i in range(len(ls)):
									if(i%4==1):
										sel.append(ls[i])
								neg = ''.join(random.sample(sel,1))
								return ' '.join([neg,l[index]])

						else:
							return l[index+2] # Present & plural (Eats)
					elif(inflect["time"]=="past"):
						return l[index]   
					else:
						return "will "+l[index] # Future
		elif(rule == "AUX"): # Auxillary
			if("type" in frame):
				word = frame["type"]
				l = [item for sublist in lexicon[rule] for item in sublist] # flattened list
				for index,w in enumerate(l):
					if(w==word):
						if "time" in inflect:
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
			else:
				# We are selecting a word. Most probably for a question
				l = [item for sublist in lexicon[rule] for item in sublist] # flattened list
				sel = [] # will select randomly from this list
				if(inflect["time"] == "past"): 
					if(inflect["polarity"] == "pos"): # Past positive : start from l[2]
						for i in range(len(l)):
							if(i%4==2):
								sel.append(l[i])
						return random.sample(sel,1)
					else: # Past negative : start from l[3]
						for i in range(len(l)):
							if(i%4==3):
								sel.append(l[i])
						return random.sample(sel,1)
				else: # time is present/future
					if(inflect["polarity"] == "pos"): # Present positive : start from l[2]
						for i in range(len(l)):
							if(i%4==0):
								sel.append(l[i])
						return random.sample(sel,1)
					else: # present negative : start from l[1]
						for i in range(len(l)):
							if(i%4==1):
								sel.append(l[i])
						return random.sample(sel,1)
								
		elif(rule == "ADJ" or rule == "PREP" or rule == "DET"): # Adjective or Preposition or Gerund
			word = frame["type"]
			for index,w in enumerate(lexicon[rule]):
				if(w==word):
					return word
		elif(rule == "TO"):
			return "to"
	
	def findWords(frame):
		inflect = []
		patientAdj = []
		agentAdj = []
		agentNoun = ""
		patientNoun = ""
		mainVerb = ""
		agentDet = ""
		patientDet = ""
		q = ""

		if("type" in frame): # main verb
			if("time" in frame):
				inflect.append(("time",frame["time"]))
			if("speechact" in frame):
				inflect.append(("speechact",frame["speechact"]))
			if("polarity" in frame):
				inflect.append(("polarity",frame["polarity"]))
			if("number" in frame):
				inflect.append(("number",frame["number"]))
			mainVerb = findWord("V",dict(inflect),{"type":frame["type"]})

		if("agent" in frame): # main agent noun
			for k,v in frame["agent"].items():
				if(k=="type"): # main noun
					agentNoun = findWord("N",frame["agent"],frame["agent"])
				elif(k in adjList):
					agentAdj.append(findWord("ADJ",{},{"type":frame["agent"][k]}))
				elif(k == "det"):
					agentDet = findWord("DET",{},{"type":frame["agent"][k]})
		if("patient" in frame): # main  patient noun
			for k,v in frame["patient"].items():
				if(k=="type"): # main patient noun
				## TODO : Not checking for plurals here
					patientNoun  = findWord("N",frame["patient"],frame["patient"])
				elif(k in adjList):
					patientAdj.append(findWord("ADJ",{},{"type":frame["patient"][k]}))
				elif(k == "det"):
					patientDet = findWord("DET",{},{"type":frame["patient"][k]})
		if("speechact" in frame): 
			if(frame["speechact"] == "question"): # append aux before and ? after sentence
				inflect = {"time":frame["time"], "polarity": frame["polarity"]} 
				q = ''.join(findWord("AUX",inflect,{}))
		
		if(q):		
			print ' '.join([q,agentDet,agentNoun,mainVerb,patientDet,patientNoun,"?"]) 
		else:
			print ' '.join([agentDet,agentNoun,mainVerb,patientDet,patientNoun])
	
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
				OrderedDict([("DET",["head","det"]),("ADJ*",["head"]),("N",["head","type"]),("PP*",["head"])])]
	
	# add rules for S
	g.append(Grammar("S",rhsRule)) 

	# loop over grammar and print rules
	for i in range(len(g)):
		Grammar.parse(g[i])


	# lexicon format
	# N : [[singular,plural]]
	# V : [[present, past, future, present-plural, past-pl, future-plural]]
	# AUX : [[present, present-neg, past, past-neg]]
	# ADJ : [list of adj] ,  ADV : [list of adv] , PREP : [list of Prep]
	lexicon = {}

	lexicon = { 
	  "N":[["potato","potatoes"],["In-N-Out","In-N-Out"],["french-fry","french-fries"],["way","ways"],
	  		["store","stores"],["we","we"],["man","men"],["peach","peaches"],["freezer","freezers"]],\
	  "V": [["cook","cooked","cooks"],["prepare","prepared","prepares"],["use","used","uses"],\
	  		["deliver","delivered","delivers"],["take","took","took"], ["complement","complemented","complements"],\
	  		["is","was","will be"],["do","did","will do"],["know","knew","knows"],["eat","ate","eats"]],
	  "AUX": [["can","cannot","could","could not"],["should","should not","should have","shouldn't have"],\
	   		 ["do","do not","did","did not"],["will","will not","would","would not"]],\
	  "ADJ": ["bold","best","large","tasty","fresh","good","whole","trans-fat-free","vegetable",\
	  		  "hot","large","red","small"],\
	  "ADV": ["individually","not"],
	  "PREP": ["at","that","we","our"],
	  "DET": ["a","an","the","that"],
	  "GER": ["regarding"],
	  "TO" : ["to"]
	}
	
	# Test cases
	#print findWord("N",{"number":"pluaral"},{"type":"potato"})
	#print findWord("V",{"time":"future","number":"plural"},{"type":"prepare"})
	#print findWord("AUX",{"time":"past","polarity":"neg"},{"type":"should"})
	#print findWord("ADJ",{},{"type":"best"})
	#print findWord("PREP",{},{"type":"at"})

	# Initialize frame
	frame = {}

	# Did the large man eat the peach?
	inRep = [("type","eat"),("agent",dict((["type","man"],["det","the"],["size","large"],["number","single"]))),\
			("patient",dict((["type","peach"],["size","small"],["color","red"],["det","a"],["number","single"]))),\
			("time","past"),("speechact","question"),("polarity","pos"),("number","single")]
	frame = dict(inRep)

	findWords(frame)

	# We do not use a freezer
	inRep = [("type","use"),("agent",{"type":"we","number":"plural"}),\
			("patient",{"type":"freezer","det":"a","number":"single"}),\
			("time","present"),("speechact","assertion"),("polarity","neg"),("number","single")]
	frame = dict(inRep)

	findWords(frame)


	# We prepare the potatoes individually.
	inRep = [("type","prepare"),("agent",{"type":"we","number":"plural"}),\
			("patient",{"type":"potato","det":"the","number":"plural"}),\
			("time","present"),("speechact","assertion"),("polarity","pos"),("number","single"),\
			("manner","individually")]
	frame = dict(inRep)
	findWords(frame)

if __name__ == '__main__':
	main()