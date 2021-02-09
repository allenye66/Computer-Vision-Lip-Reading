

#DELETE ALL THE CASE NOT FOUND INAUDIO LINES FIRST
#DELETE ALL THE CASE NOT FOUND INAUDIO LINES FIRST
#DELETE ALL THE CASE NOT FOUND INAUDIO LINES FIRST
#DELETE ALL THE CASE NOT FOUND INAUDIO LINES FIRST
#DELETE ALL THE CASE NOT FOUND INAUDIO LINES AND THE UNKCLEAR WORDS
#"alignedWord": "<unk>"
#"case": "not-found-in-audio"


#THE LENGTH OF THE CLEAN CSV HAS TO MATCH THE LENGTH OF "ALIGNED_WORD_ARR"

import csv
input_text = open('/Users/allen/Desktop/Automated-Speech-Recognition/align_example.txt')


aligned_word_arr = []
word_arr = []
fail_words = 0



#the text file contains words that couldn't be transcriped, for example: 
'''
{
      "case": "not-found-in-audio",
      "endOffset": 1587,
      "startOffset": 1582,
      "word": "tried"
},
'''


#first remove all these instances, subsequent 4 lines
'''
for line in input_text:
	if '"case": "not-found-in-audio",' in line:
		fail_words+=1
print(fail_words)
'''


line_num = 0
for line in input_text:
	#print(line)
	line_num += 1
	if '"alignedWord":' in line:
		aligned_word_arr.append(line_num)
	if '"word":' in line:
		word_arr.append(line_num)

print(len(aligned_word_arr))
print(len(word_arr))
#should equal zero and have 1:1 ratio
print(len(aligned_word_arr)-len(word_arr))
