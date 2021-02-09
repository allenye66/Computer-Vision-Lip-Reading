import csv
import math

fileIn = 'example_phoneme_timestamps.csv'
fileOut = 'example_phoneme_framestamps.csv'
fps = 30
with open(fileOut, 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(["Phoneme", "Start Frame", "End Frame"])
	with open(fileIn) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count != 0:
				phoneme = row[0]
				start_time = row[1]
				end_time = row[2]
				start_frame = math.ceil(float(start_time) * fps)
				end_frame = math.floor(float(end_time) * fps)
				writer.writerow([phoneme, start_frame, end_frame])
				print(f'Phoneme: {phoneme} | Start Frame: {start_frame} | End Frame: {end_frame}')
			line_count = line_count + 1