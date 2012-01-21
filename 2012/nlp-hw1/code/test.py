#!/usr/bin/env python
# Jan 21, 1:30am Got simple rules to work
# TODO: implement stuff like PP*, ADJ* (take care of *)

import random

def main():
	num_grammar_rules = 10
	grammar = []
	grammar.append("S")					# 0
	grammar.append(["NP","VP"]) 		# 
	grammar.append("S")					# 2
	grammar.append(["NP"]) 				# 
	grammar.append("NP")				# 4
	grammar.append(["N","PP"]) 			# 
	grammar.append("NP")				# 6	
	grammar.append(["V","PP"]) 			# 
	grammar.append("VP")				# 8	
	grammar.append(["V","PP"])			# 
	grammar.append("N")					# 10
	grammar.append(["boy","girl"])		# 
	grammar.append("V")					# 12
	grammar.append(["screw","do"])		# 
	grammar.append("PP")				# 14
	grammar.append(["in","on"])	
	

	stack = ["S"]
	sentence = []

	def selectRandomRule(rule):
		i = -1
		selected = []
		try:
			while 1:
				i = grammar.index(rule,i+1)
				selected.append(i)
		except ValueError:
			pass
		selectedRule = random.sample(selected,1)[0]
		return selectedRule
	
	def selectRandomWord(ruleNumber):
		return random.sample(grammar[ruleNumber+1],1)[0]

	def expand(stack):
		selectedRule = selectRandomRule(stack[len(stack)-1])
		if(selectedRule <= 8):
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
		
	i = 0
	while stack:
		expand(stack)
		print "Stack is now: "
		print stack
		i = i + 1
	
	# Now stack is expanded for first time

	print "Sentence is : "
	print sentence
		
if __name__ == '__main__':
	main()
