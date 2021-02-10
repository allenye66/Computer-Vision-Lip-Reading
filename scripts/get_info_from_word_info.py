array = ['"alignedWord": "if",', '"case": "success",', '"end": 0.33,', '"endOffset": 3,', '"phones": [', '{', '"duration": 0.09,', '"phone": "ih_B"', '},', '{', '"duration": 0.1,', '"phone": "f_E"', '}', '],', '"start": 0.14,', '"startOffset": 1,', '"word": "If"']
phonemes = []
start_times = []
end_times = []
durations = []
for k in array:
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
print(durations)