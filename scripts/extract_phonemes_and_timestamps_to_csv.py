

#DELETE ALL THE CASE NOT FOUND INAUDIO LINES FIRST
#DELETE ALL THE CASE NOT FOUND INAUDIO LINES FIRST
#DELETE ALL THE CASE NOT FOUND INAUDIO LINES FIRST
#DELETE ALL THE CASE NOT FOUND INAUDIO LINES FIRST
#DELETE ALL THE CASE NOT FOUND INAUDIO LINES AND THE UNKCLEAR WORDS
#"alignedWord": "<unk>"
#"case": "not-found-in-audio"


#THE LENGTH OF THE CLEAN CSV HAS TO MATCH THE LENGTH OF "ALIGNED_WORD_ARR"


import csv
input_text = open('align_example.txt')
aligned_word_arr = []
word_arr = []
fail_words = 0



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



with open('align_example.txt') as f:
    text = f.readlines()
text = [x.strip() for x in text] 
#print((content)[1])

#text=open('align_example.txt').readlines()
#text = [line.strip() for line in text]
#with open('align_example.txt') as f:
#    text = f.read().splitlines() 
#print(text)

#python /Users/allen/Desktop/Automated-Speech-Recognition/scripts/extract_phonemes_and_timestamps_to_csv.py > /Users/allen/Desktop/Automated-Speech-Recognition/scripts/asdf.txt 


current_time = 0
for i in range(len(aligned_word_arr)):
	#print(aligned_word_arr[i]-1, word_arr[i]) # has the -1 because we need to included "alignedword"
	current_word_info = []
	for j in range(aligned_word_arr[i]-1, word_arr[i]):
		current_word_info.append(text[j])
	#print(current_word_info)
	phonemes = []
	start_times = []
	end_times = []
	durations = []
	for k in current_word_info:
		if "phones" not in k:
			if "phone" in k:
				phonemes.append(k[10:len(k)-3])
		if "startOffset" not in k:
			if "start" in k:
				start_times.append(float(k[9:len(k)-1]))

		
		if "duration" in k:
			durations.append(float(k[12:len(k)-1]))
		#add to the end
		#if "endOffset" not in i:
	#		if "end" in i:
	#			end_times.append(float(i[7:len(i)-1]))

	for k in range(len(durations)-1):
		start_times.append(start_times[k-1]+durations[k])

	end_times = start_times[1:]
	end_times.append(start_times[-1]+durations[-1])
	print(phonemes)
	print(start_times)
	print(end_times)
	#print(durations)


#	print(current_word_info)
#	for i in current_word_info:
#		print(i)	


	#start_time =
	#end_time = 
	#csv save row



