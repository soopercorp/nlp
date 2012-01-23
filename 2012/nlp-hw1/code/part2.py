#!/usr/bin/env python
# @author Hardik Ruparel
# @copyright All Rights Reserved
# @todo Testing

import random

def main():
	
	gramlex = [] # Single list for grammar and lexicon
	
	# GRAMMAR
	gramlex.append("S")					# 0
	gramlex.append(["NP","VP"]) 		# 
	gramlex.append("S")					# 2
	gramlex.append(["AUX","NP","VP"]) 	#
	gramlex.append("S")					# 4
	gramlex.append(["NP","AUX","VP"]) 	#
	gramlex.append("NP")				# 6
	gramlex.append(["DET","ADJ*","N","PP*"])
	gramlex.append("NP")				# 8
	gramlex.append(["N","PP*"]) 			
	gramlex.append("NP")				# 10
	gramlex.append(["PRO"]) 			#
	gramlex.append("VP")				# 12
	gramlex.append(["V","NP"])			#
	gramlex.append("VP")				# 14
	gramlex.append(["V","NP","PP*"])		
	gramlex.append("VP")				# 16
	gramlex.append(["V","ADV"])			#
	gramlex.append("PP*")				# 18
	gramlex.append(["P","NP"])			#
	

	# LEXICON
	gramlex.append("AUX")				
	gramlex.append(["does","can","may","will"])		
	gramlex.append("N") 
	gramlex.append(["boy","girl","house","car"]) 
	gramlex.append("V")
	gramlex.append(["fly","kick","kiss"]) 
	gramlex.append("P")
	gramlex.append(["in","on","between"])	
	gramlex.append("PRO")
	gramlex.append(["I","you","he","it"])	
	gramlex.append("DET") 
	gramlex.append(["a","an","the"])
	gramlex.append("ADJ*") 
	gramlex.append(["awesome","good","bad"])
	gramlex.append("ADV") 
	gramlex.append(["slowly","fast","incredibly"])


	stack = ["S"]
	sentence = []
	seed = "001" 	# seed for random choice between 0 an 1 P(0) = 2/3. P(1) = 1/3
	"""
	Selects a random rule from one of the matching rules. 
	"""
	def selectRandomRule(rule):
		i = -1
		selected = []
		try:
			while 1:
				i = gramlex.index(rule,i+1)
				selected.append(i)
		except ValueError:
			pass
		selectedRule = random.sample(selected,1)[0] # Selects a random (rule number) element from list
		return selectedRule
	
	
	"""
	Selects a random word from one of the lexicon definitions.
	"""
	def selectRandomWord(ruleNumber):
		return random.sample(gramlex[ruleNumber+1],1)[0] # returns the string form of selected random word

	"""
	Expand the stack.
	"""
	def expand(stack):
		starChoiceMade = 0 # Chose the * in PP* etc. or not
		selectedRule = selectRandomRule(stack[len(stack)-1])
		if(selectedRule <= 18):  							# After this we have the lexicon
			if not "*" in gramlex[selectedRule]:
				starChoiceMade = 1
				print "Expanding rule number: {}".format(selectedRule)
				print "Executing rule: "+ gramlex[selectedRule]+"-> "+str(gramlex[selectedRule+1])
			else:
				starChoiceMade = int(random.choice(seed))
				print "Chose {}".format(starChoiceMade)
				if (starChoiceMade):
					print "Expanding rule number: {}".format(selectedRule)
					print "Executing rule: "+ gramlex[selectedRule]+"-> "+str(gramlex[selectedRule+1])
			stack.pop() # Pop the rule just executed
			if starChoiceMade:
				for rule in reversed(gramlex[selectedRule+1]): # So first rule is at head of stack and popped 1st
					stack.append(rule)
		else:
			if not "*" in gramlex[selectedRule]:
				word = selectRandomWord(selectedRule)
				starChoiceMade = 1
			else:
				starChoiceMade = int(random.choice(seed))
				print "Chose {}".format(starChoiceMade)
				if (starChoiceMade):
					word = selectRandomWord(selectedRule)	
			stack.pop() # Pop the lexicon word
			if(starChoiceMade):
				sentence.append(word)
				print "Appended word : "+word+" to sentence"
				print "Sentence is: "
				print sentence
		
	while stack:
		expand(stack)
		print "Stack is now: "
		print stack
	
	print "Finally, Sentence is : "
	print ' '.join(sentence)
		
if __name__ == '__main__':
	main()