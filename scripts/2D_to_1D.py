import pandas as pd
import csv
import sys
import numpy as np

fileOut = '../data/final_labeled_frames.csv'
fileIn = '../data/labeled_frames.csv'
csv.field_size_limit(sys.maxsize)
np.set_printoptions(threshold=sys.maxsize)

with open(fileOut, 'w', newline='') as file:
	writer = csv.writer(file)
	title = []
	title.append("Phoneme")
	for i in range(19200):
		title.append("Pixel " + str(i + 1))
	writer.writerow(title)
	with open(fileIn) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			line_count = 0
			for row in csv_reader:
				if line_count != 0:
					next_row = []
					next_row.append(row[0])
					image = np.array(row[1].replace('[', '').replace(']', '').split()).astype(np.float).astype(np.uint8)
					# if len(image) > 19200:
					# 	print(image)
					# 	break
					for value in image:
						next_row.append(value)
					writer.writerow(next_row)
					print(f'line_count: {line_count}')
				line_count = line_count + 1