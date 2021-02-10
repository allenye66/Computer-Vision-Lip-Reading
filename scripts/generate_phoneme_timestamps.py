import csv

fileOut = 'data/phoneme_timestamps.csv'
fileIn = 'data/align_example.txt'

with open(fileOut, 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(["Phoneme", "Start Time", "End Time"])

	with open(fileIn) as fp:
		line = fp.readline()
		line_num = 0
		duration_arr = []
		phoneme_arr = []
		while line:
			if line_num > 2:
				if 'duration' in line:
					duration = line[line.index(':')+2:line.index(',')]
					duration_arr.append(round(float(duration), 2))
					line = fp.readline()
					line_num = line_num + 1
					phoneme = line[line.index(':')+3:line.index('_')]
					phoneme_arr.append(phoneme)
				if 'start\"' in line:
					start_time = round(float(line[line.index(':')+2:line.index(',')]), 2)
					while phoneme_arr:
						end_time = round(start_time + duration_arr.pop(0), 2)
						writer.writerow([phoneme_arr.pop(0), start_time, end_time])
						start_time = end_time

			
			line = fp.readline()
			line_num = line_num + 1

