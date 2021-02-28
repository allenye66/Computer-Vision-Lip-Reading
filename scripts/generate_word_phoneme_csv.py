import csv

fileOut = 'data/phonemes.csv'
fileIn = 'data/phoneme_dictionary.txt'

with open(fileOut, 'w', newline='') as file:

	writer = csv.writer(file)
	writer.writerow(["Word", "Phonemes"])

	with open('phoneme_dictionary.txt') as fp:
		line = fp.readline()
		cnt = 1
		while line:
			word = ""
			phonemes = ""
			wordAdded = False
			
			for i in line.split():
				if not wordAdded:
					word = i
					wordAdded = True
				else:
					phonemes = phonemes + i + " "
			phonemes = phonemes[:-1]

			writer.writerow([word, phonemes])
			
			cnt += 1
			word = ""
			phonemes = ""
			line = fp.readline()