#!/usr/bin/env python
# @author Hardik Ruparel
# @copyright All Rights Reserved
# @info:1. Parts of Speech tagged in reference to Penn Treebank :
# 		http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

from collections import OrderedDict
from sys import stdout
import random

# frame Parts-of-Speech list
nounList = ["information","location","instrument","source","destination",\
			"beneficiary","time","location","attribute","experiencer","agent","patient"]
adjList = ["color","age","size","quality","style"]
advList = ["manner"]
pronounList = ["owner"]

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
	
	"""
	Returns correct word from lexicon
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
								retword = l[index] # Present (Eat)
							else:
								# have to find an aux
								ls = [item for sublist in lexicon["AUX"] for item in sublist] # flattened list
								sel = [] # will select randomly from this list
								for i in range(len(ls)):
									if(i%4==1):
										sel.append(ls[i])
								neg = ''.join(random.sample(sel,1))
								retword = ' '.join([neg,l[index]])
								ls = [item for sublist in lexicon["AUX"] for item in sublist] # flattened list
								for i,w in enumerate(ls):
									if(w == inflect["aux"]):
										neg = ls[i+1]
								retword = ' '.join([neg,l[index]])

						else:
							retword = l[index+2] # Present & plural (Eats)
					elif(inflect["time"]=="past"):
						retword = l[index]   
					else:
						retword = "will "+l[index] # Future
			return retword
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
				
				#sel = [] # will select randomly from this list
				if(inflect["time"] == "past"): 
					if(inflect["polarity"] == "pos"): # Past positive : start from l[2]
						#for i in range(len(l)):
						#	if(i%4==2):
						#		sel.append(l[i])
						#return random.sample(sel,1)
						for i,w in enumerate(l):
							if(w == inflect["aux"]):
								neg = l[i]
						return neg
					else: # Past negative : start from l[3]
						#for i in range(len(l)):
						#	if(i%4==3):
						#		sel.append(l[i])
						#return random.sample(sel,1)
						for i,w in enumerate(l):
							if(w == inflect["aux"]):
								neg = l[i+1]
						return neg
				else: # time is present/future
					if(inflect["polarity"] == "pos"): # Present positive : start from l[2]
						#for i in range(len(l)):
						#	if(i%4==0):
						#		sel.append(l[i])
						#return random.sample(sel,1)
						for i,w in enumerate(l):
							if(w == inflect["aux"]):
								neg = l[i]
						return neg
					else: # present negative : start from l[1]
						#for i in range(len(l)):
						#	if(i%4==1):
						#		sel.append(l[i])
						#return random.sample(sel,1)
						for i,w in enumerate(l):
							if(w == inflect["aux"]):
								neg = l[i]
						return neg
		elif(rule == "ADJ" or rule == "PREP" or rule == "DET" or rule == "ADV"): # Adjective or Preposition or Gerund
			word = frame["type"]
			for index,w in enumerate(lexicon[rule]):
				if(w==word):
					return word
		elif(rule == "PRO"):
			for index,w in enumerate(frame):
				if(w in pronounList):
					return frame[w]
		
	"""
	Constructs the sentence given an input frame.
	Calls the findWord function repeatedly.
	"""
	def buildSentence(frame):
		inflect = []
		patientAdj = []
		agentAdj = []
		agentNoun = ""
		patientNoun = ""
		mainVerb = ""
		agentDet = ""
		patientDet = ""
		auxWord = ""
		q = ""
		adverb = ""
		proNounFlag = 0 # eg noun is "them" 
		roleFlag = 0 # there is a preposition and PP[role head] is activated
		proNoun = ""
		secAdj = "" # secondary Adjective
		auxFlag = 0


		if("type" in frame): # main verb
			"""if("time" in frame):
				inflect.append(("time",frame["time"]))
			if("speechact" in frame):
				inflect.append(("speechact",frame["speechact"]))
			if("polarity" in frame):
				inflect.append(("polarity",frame["polarity"]))
			if("number" in frame):
				inflect.append(("number",frame["number"]))
			if("aux" in frame):
				inflect.append((("aux"),frame["aux"]))"""

			mainVerb = findWord("V",buildInflect(frame),{"type":frame["type"]})

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
					if(patientNoun=="them"):
						proNounFlag = 1
				elif(k in adjList):
					patientAdj.append(findWord("ADJ",{},{"type":frame["patient"][k]}))
				elif(k == "det"):
					patientDet = findWord("DET",{},{"type":frame["patient"][k]})
		if("speechact" in frame): 
			if(frame["speechact"] == "question"): # need to find aux, eg Should? Did? Could?
				if("aux" in frame):
					inflect = {"time":frame["time"], "polarity": frame["polarity"], "aux": frame["aux"]}
				else:	
					inflect = {"time":frame["time"], "polarity": frame["polarity"]} 
				q = ''.join(findWord("AUX",inflect,{}))
		if("manner" in frame):
			adverb = findWord("ADV",{},{"type":frame["manner"]})
		if("role" in frame):
			roleType = findPrep(frame) # eg destination
			rolePrep = frame["role"]["type"] # eg to
			roleNoun = findWord("N",frame["role"][roleType],frame["role"][roleType]) # eg stores
			#print frame["role"]
			for v in frame["role"][roleType]:
				if(v in pronounList):
					proNoun = findWord("PRO",frame["role"][roleType],frame["role"][roleType])
				elif(v in adjList):
					secAdj = findWord("ADJ", {} , {"type":frame["role"][roleType][v]})
			roleFlag = 1

		
		# Have to fix this
		if(q):		
			return ' '.join([q,agentDet,' '.join(agentAdj),agentNoun,mainVerb,patientDet,' '.join(patientAdj),patientNoun,adverb,"?"]) 
		else:
			if(proNounFlag == 1):
				if(roleFlag == 1):
					return [agentDet,' '.join(agentAdj),agentNoun,mainVerb,patientDet,patientNoun,' '.join(patientAdj),adverb,rolePrep,proNoun,secAdj,roleNoun]
				else:
					return [agentDet,' '.join(agentAdj),agentNoun,mainVerb,patientDet,patientNoun,' '.join(patientAdj),adverb]
			else:
				return [agentDet,' '.join(agentAdj),agentNoun,mainVerb,patientDet,' '.join(patientAdj),patientNoun,adverb]		
		
	"""
	Builds Inflect
	"""

	def buildInflect(frame):
		inflect = []
		if("time" in frame):
			inflect.append(("time",frame["time"]))
		if("speechact" in frame):
			inflect.append(("speechact",frame["speechact"]))
		if("polarity" in frame):
			inflect.append(("polarity",frame["polarity"]))
		if("number" in frame):
			inflect.append(("number",frame["number"]))
		if("aux" in frame):
			inflect.append((("aux"),frame["aux"]))
		return dict(inflect)


	"""
	Finds the appropriate Preposition
	"""
	def findPrep(frame):
		if("destination" in frame["role"]):
			return "destination"
		if("inwhat" in frame["role"]):
			return "inwhat"

	"""
	Expands the grammar
	"""
	def expand(grammar,stack,frame):
		sentence = []
		rest = buildSentence(frame)
		if("aux" in frame and frame["speechact"] == "assertion"): # Caught Aux in beginning
			stack.pop()
			searchFrame = {"aux":frame["aux"]}
			aux = findWord("AUX",buildInflect(frame),searchFrame)
			print aux
		rest = buildSentence(frame)
		print rest

	def backTrack(sentence):
		pass

		"""print stack
		if(stack[len(stack)-1] == "S"):
			if("aux" not in frame):
				execRule(grammar[0].rhs[0],stack)
			else:
				execRule(grammar[0].rhs[1],stack)
			

	def execRule(subg,stack):
		stack.pop()
		for lhs in reversed(subg):
			stack.append(lhs)"""




		

		
		

	


	"""
	Executes one rule
	
	def execRule(grammar,stack,frame):
		for k,v in enumerate(grammar):
			if v.lhs == stack[len(stack)-1]: # top element of stack - to be expanded. Initially S
				# Found item to be expanded, now need to select rule
				stack.pop()

				break
	"""

	# initialize list of grammar rules
	g = []
	
	# add items
	# S
	rhsRule = 	[OrderedDict([("NP",["head","agent"]),("VP",["head"])]),\
				OrderedDict([("AUX",["head","agent"]),("NP",["head","agent"]),("VP",["head"])]),\
				OrderedDict([("NP",["head","agent"]),("AUX",["head","agent"]),("VP",["head"])])]
	
	g.append(Grammar("S",rhsRule))
	
	# NP
	rhsRule = 	[OrderedDict([("DET",["head","det"]),("ADJ*",["head"]),("N",["head","type"]),("PP*",["head"])]),\
				OrderedDict([("PRO",["head"])]),\
				OrderedDict([("N",["head","type"]),("PP*",["head"])])]
	
	g.append(Grammar("NP",rhsRule))

	# VP
	rhsRule = 	[OrderedDict([("V",[["head","type"],["head","time"]]),("NP",["head","patient"])]),\
				OrderedDict([("V",[["head","type"],["head","time"]]), ("NP",["head","patient"]), ("PP*",["head"])]),\
				OrderedDict([("N",["head","type"]),("PP*",["head"])])]
	
	g.append(Grammar("VP",rhsRule))

	# PP
	rhsRule = 	[OrderedDict([("PREP",["head","role"]),("NP",["head"])])]
	
	g.append(Grammar("PP*",rhsRule))

	# loop over grammar and output rules
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
	  		["store","stores"],["we","we"],["man","men"],["peach","peaches"],["freezer","freezers"],["them","them"],
	  		["vegetable oil","vegetable oil"]],\
	  "V": [["cook","cooked","cooks"],["prepare","prepared","prepares"],["use","used","uses"],\
	  		["deliver","delivered","delivers"],["take","took","took"], ["complement","complemented","complements"],\
	  		["is","was","will be"],["do","did","will do"],["know","knew","knows"],["eat","ate","eats"],\
	  		["feel","felt","will feel"]],
	  "AUX": [["can","cannot","could","could not"],["should","should not","should have","shouldn't have"],\
	  		["so","so","so","so"], ["do","do not","did","did not"],["will","will not","would","would not"],
	  		["and","and","and","and"], ["then","then","then","then"]],\
	  "ADJ": ["bold","best","large","tasty","fresh","good","whole","trans-fat-free",\
	  		  "hot","large","red","small","new"],\
	  "ADV": ["individually","not","slowly"],
	  "PREP": ["at","that","we","our"],
	  "DET": ["a","an","the","that"],
	  "GER": ["regarding"],
	  "PRO" : ["our","we"]
	}
	
	# Initialize frame
	frame = {}

	# Did the large man eat the small red peach slowly?
	inRep = [("type","eat"),("agent",dict((["type","man"],["det","the"],["size","large"],["number","single"]))),\
			("patient",dict((["type","peach"],["size","small"],["color","red"],["det","a"],["number","single"]))),\
			("time","past"),("speechact","question"),("polarity","pos"),("number","single"),("aux","did"),("manner","slowly")]
	frame = dict(inRep)

	#print buildSentence(frame)

	# We do not use a freezer
	inRep = [("type","use"),("agent",{"type":"we","number":"plural"}),\
			("patient",{"type":"freezer","det":"a","number":"single"}),\
			("time","present"),("speechact","assertion"),("polarity","neg"),("aux","do"),("number","single")]
	frame = dict(inRep)

	#print buildSentence(frame)
	stack = ["S"]
	#expand(g,stack,frame)


	# We prepare the potatoes individually.
	inRep = [("type","prepare"),("agent",{"type":"we","number":"plural"}),\
			("patient",{"type":"potato","det":"the","number":"plural"}),\
			("time","present"),("speechact","assertion"),("polarity","pos"),("number","single"),\
			("manner","individually")]
	frame = dict(inRep)
	#expand(g,stack,frame)


	# So we use fresh large potatoes
	inRep = [("type","use"),("agent",{"type":"we","number":"plural"}),\
			("patient",{"type":"potato","number":"plural","quality":"fresh","size":"large"}),\
			("time","present"),("speechact","assertion"),("polarity","pos"),("number","single"),("aux","so")]

	frame = dict(inRep)
	#buildSentence(frame)

	stack = ["S"]
	#expand(g,stack,frame)

	# And we deliver them fresh to our stores.
	inRep = [("type","deliver"),("agent",{"type":"we","number":"plural"}),\
			("patient",{"type":"them","number":"plural","quality":"fresh"}),\
			("time","present"),("speechact","assertion"),("polarity","pos"),("number","single"),("aux","and"),\
			("role",{"type":"to","destination":{"type":"store","number":"plural","owner":"our"}})]

	frame = dict(inRep)

	stack = ["S"]
	#expand(g,stack,frame)


	# Then we cook them in trans-fat-free vegetable oil
	inRep = [("type","cook"),("agent",{"type":"we","number":"plural"}),\
			("patient",{"type":"them","number":"plural"}),\
			("time","present"),("speechact","assertion"),("polarity","pos"),("number","single"),("aux","then"),\
			("role",{"type":"in","inwhat":{"type":"vegetable oil","number":"single","style":"trans-fat-free"}})]
	
	frame = dict(inRep)

	stack = ["S"]
	while(stack):
		expand(g,stack,frame)

	# Every day, we take whole new potatoes
	inRep = [("type","take"),("agent",{"type":"we","number":"plural"}),\
			("patient",{"type":"potato","number":"plural","style":"whole","age":"new"}),\
			("time","present"),("speechact","assertion"),("polarity","pos"),("number","single"),("aux","Every day")]
	
	frame = dict(inRep)

	stack = ["S"]
	#expand(g,stack,frame)


	# Regarding french-fries, we feel that fresh is the best way.
	inRep = [("type","feel"),("agent",{"type":"we","number":"plural"}),\
			("patient",{"type":"french-fry","number":"plural","style":"whole","age":"new"}),\
			("time","present"),("speechact","assertion"),("polarity","pos"),("number","single"),("aux","Every day")]
	
	frame = dict(inRep)

	stack = ["S"]
	#expand(g,stack,frame)
	

if __name__ == '__main__':
	main()