#!/usr/bin/env python
# @author Hardik Ruparel
# @copyright All Rights Reserved
# @todo Testing

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
	grammar.append(["DET","ADJ*","N","PP*"])
	grammar.append("NP")				# 8
	grammar.append(["N","PP*"]) 			
	grammar.append("NP")				# 10
	grammar.append(["PRO"]) 			#
	grammar.append("VP")				# 12
	grammar.append(["V","NP"])			#
	grammar.append("VP")				# 14
	grammar.append(["V","NP","PP*"])		
	grammar.append("VP")				# 16
	grammar.append(["V","ADV"])			#
	grammar.append("PP*")				# 18
	grammar.append(["P","NP"])			#
	

	# LEXICON
	grammar.append("AUX")				
	grammar.append(["does","can","may","will"])		
	grammar.append("N") 
	grammar.append(["boy","girl","house","car"]) 
	grammar.append("V")
	grammar.append(["fly","kick","kiss"]) 
	grammar.append("P")
	grammar.append(["in","on","between"])	
	grammar.append("PRO")
	grammar.append(["I","you","he","it"])	
	grammar.append("DET") 
	grammar.append(["a","an","the"])
	grammar.append("ADJ*") 
	grammar.append(["awesome","good","bad"])
	grammar.append("ADV") 
	grammar.append(["slowly","fast","incredibly"])


	stack = ["S"]
	sentence = []
	seed = "001" 	# seed for random choice between 0 an 1
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
		selectedRule = random.sample(selected,1)[0] # Selects a random (rule number) element from list
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
		choiceMade = 0
		selectedRule = selectRandomRule(stack[len(stack)-1])
		if(selectedRule <= 18):  							# After this we have the lexicon
			if not "*" in grammar[selectedRule]:
				choiceMade = 1
				print "Expanding rule number: {}".format(selectedRule)
				print "Executing rule: "+ grammar[selectedRule]+"-> "+str(grammar[selectedRule+1])
			else:
				choiceMade = int(random.choice(seed))
				print "Chose {}".format(choiceMade)
				if (choiceMade):
					print "Expanding rule number: {}".format(selectedRule)
					print "Executing rule: "+ grammar[selectedRule]+"-> "+str(grammar[selectedRule+1])
			stack.pop() # Pop the rule just executed
			if choiceMade:
				for rule in reversed(grammar[selectedRule+1]): # So first rule is at head of stack and popped 1st
					stack.append(rule)
		else:
			if not "*" in grammar[selectedRule]:
				word = selectRandomWord(selectedRule)
				choiceMade = 1
			else:
				choiceMade = int(random.choice(seed))
				print "Chose {}".format(choiceMade)
				if (choiceMade):
					word = selectRandomWord(selectedRule)	
			stack.pop() # Pop the lexicon word
			if(choiceMade):
				sentence.append(word)
				print "Appended word : "+word+" to sentence"
				print "Sentence is: "
				print sentence
		
	while stack:
		expand(stack)
		print "Stack is now: "
		print stack
	
	print "Finally, Sentence is : "
	print sentence
		
if __name__ == '__main__':
	main()