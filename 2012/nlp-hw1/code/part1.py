#!/usr/bin/env python

import random

def main():
	
	# GRAMMAR
	grammar = []
	grammar.append("S")					# 0
	grammar.append(["NP","VP"]) 		# 
	grammar.append("S")					# 2
	grammar.append(["AUX","NP","VP"]) 	#
	grammar.append("S")					# 4
	grammar.append(["NP","AUX","VP"]) 	#
	grammar.append("NP")				# 6
	grammar.append(["DET","ADJ","N","PP"])
	grammar.append("NP")				# 8
	grammar.append(["N","PP"]) 			
	grammar.append("NP")				# 10
	grammar.append(["PRO"]) 			#
	grammar.append("VP")				# 12
	grammar.append(["V","NP"])			#
	grammar.append("VP")				# 14
	grammar.append(["V","NP","PP"])		
	grammar.append("VP")				# 16
	grammar.append(["V","ADV"])			#
	
	# LEXICON
	grammar.append("AUX")				
	grammar.append(["does","can","may","will"])		
	grammar.append("N") 
	grammar.append(["boy","girl","house","car"]) 
	grammar.append("V")
	grammar.append(["fly","kick","kiss"]) 
	grammar.append("PP")
	grammar.append(["in","on","between"])	
	grammar.append("PRO")
	grammar.append(["I","you","he","it"])	
	grammar.append("DET") 
	grammar.append(["a","an","the"])
	grammar.append("ADJ") 
	grammar.append(["awesome","good","bad"])
	grammar.append("ADV") 
	grammar.append(["slowly","fast","incredibly"])


	stack = ["S"]
	sentence = []

	"""
	Selects a random rule from one of the matching rules. 
	"""
	def selectRandomRule(rule):
		i = -1
		selected = []
		try:
			while 1:
				i = grammar.index(rule,i+1)
				selected.append(i)
		except ValueError:
			pass
		selectedRule = random.sample(selected,1)[0] # Selects a random element from list
		return selectedRule
	
	
	"""
	Selects a random word from one of the lexicon definitions.
	"""
	def selectRandomWord(ruleNumber):
		return random.sample(grammar[ruleNumber+1],1)[0] # returns the string form of selected random word

	
	"""
	Expand the stack.
	"""
	def expand(stack):
		selectedRule = selectRandomRule(stack[len(stack)-1])
		if(selectedRule <= 16):
			print "Expanding rule number: {}".format(selectedRule)
			print "Executing rule: "+ grammar[selectedRule]+"-> "+str(grammar[selectedRule+1])
			stack.pop() # Pop the rule just executed
			for rule in reversed(grammar[selectedRule+1]):
				stack.append(rule)
		else:
			word = selectRandomWord(selectedRule)
			stack.pop() # Pop the lexicon word
			sentence.append(word)
			print "Appended word : "+word+" to sentence"
		
	while stack:
		expand(stack)
		print "Stack is now: "
		print stack
	
	print "Sentence is : "
	print sentence
		
if __name__ == '__main__':
	main()