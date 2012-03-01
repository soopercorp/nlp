#! /usr/bin/python -tt

import sys


def main():
  args = sys.argv[1:]
  print args
  if len(args) !=2 :
    print 'usage: inputfile outputfile'
    sys.exit(1)
  input_file = open(args[0],'rU')
  output_file = open(args[1],'rU')
  
  while True:
    if output_file.readline().strip() == '@data':
      break;
    
  #evaluation_file
  eval_list = []
  for line in input_file:
    input_word_feat = (line.strip()).split(' ')
    word = input_word_feat[0] 
    if word != '':
      output_vector = output_file.readline().strip().split(',')
      word += ' ' + output_vector[-1] + ' '+ output_vector[-2]
    eval_list.append(word)
  input_file.close()
  output_file.close()
  eval_text = '\n'.join(eval_list)  
  evaluation_file = open('hr.output','w')
  evaluation_file.write(eval_text)
  evaluation_file.close()

  
if __name__ =='__main__':
  main()  