#to clean csv file, add header line for Word, Phonemes, Start, End, delete any rows that have <unk> or are empty,

import csv


#add a new header
with open('/Users/allen/Desktop/Automated-Speech-Recognition/align_example.csv',newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
with open('/Users/allen/Desktop/Automated-Speech-Recognition/align_example_with_header.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['Word','Phonemes', 'Start', 'End'])
    w.writerows(data)


#delete rows containing bad data


good_data = 0
unk = 0
import csv
with open('/Users/allen/Desktop/Automated-Speech-Recognition/align_example_with_header.csv', 'r') as f, open('/Users/allen/Desktop/Automated-Speech-Recognition/align_clean.csv', 'w') as out:
	writer = csv.writer(out)
	reader = csv.reader(f, delimiter=',')
	for row in reader:
		#print(row[1])
		if row[1]: #if not empty string
			if "<unk>" not in row:
				writer.writerow(row)
				print(row[1])
				good_data += 1

		if "<unk>" in row:
			unk +=1

print(unk)
print(good_data)


#64 blank lines(grep -c "^$" /Users/allen/Desktop/column_1.txt)
#13 unks
#77 bad data