import csv
import sys

def phoneme_to_word(phonemes):
	with open('/Users/allen/Desktop/Automated-Speech-Recognition/phonemes.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if (row[1] == phonemes):
				return row[0]

if __name__=="__main__":
	print(phoneme_to_word(sys.argv[1]))