import csv

def get_word(phonemes):
	with open('../data/phonemes.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		as_string = ''
		for i in phonemes:
			as_string = as_string + i.upper() + ' '
		as_string = as_string[:-1]
		line_count = 0
		for row in csv_reader:
			if line_count != 0:
				if row[1] == as_string:
					return row[0]
			line_count = line_count + 1

if __name__ == '__main__':