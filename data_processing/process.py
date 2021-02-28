import csv
import cv2
import dlib
import csv
import os.path
import math
import sys
import numpy


'''
Parses through text output from Gentle forced aligner and generates csv file 
with start and end time of each phoneme
'''
def phonemes_and_timestamps_to_csv(fileIn, fileOut):
	
	with open(fileOut, 'w', newline='') as write_file:
		
		writer = csv.writer(write_file)
		writer.writerow(["Phoneme", "Start Time", "End Time"])

		with open(fileIn) as read_file:
			
			line = read_file.readline()
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
				line = read_file.readline()
				line_num += 1


'''
Reads csv file with timestamps of each phoneme and generates csv file
with start and end frame of each phoneme
'''
def frames_per_phoneme(fileIn, fileOut):
	
	fps = 24	# fps of video feed
	
	with open(fileOut, 'w', newline='') as write_file:

		writer = csv.writer(write_file)
		writer.writerow(["Phoneme", "Start Frame", "End Frame"])

		with open(fileIn) as read_file:

			csv_reader = csv.reader(read_file, delimiter=',')
			line_count = 0
			for row in csv_reader:
				if line_count != 0:
					phoneme = row[0]
					start_time = row[1]
					end_time = row[2]
					start_frame = math.ceil(float(start_time) * fps)
					end_frame = math.floor(float(end_time) * fps)
					writer.writerow([phoneme, start_frame, end_frame])
				line_count += 1


'''
Iterates through each frame in the video feed and segments out the mouth using 
OpenCV Haar Cascade facial features model. Reads csv file with start and end frame 
of each phoneme in order to label each frame with a phoneme. Outputs a csv file
with each row containing a phoneme, and 4096 pixels representing the image associated with 
that phoneme.
'''
def crop_mouth(fileIn, videoPath, fileOut):
	
	numpy.set_printoptions(threshold=sys.maxsize)
	
	with open(fileOut, 'w', newline='') as write_file:
		
		writer = csv.writer(write_file)
		title = []
		title.append("Phoneme")
		for i in range(4096):
			title.append("Pixel " + str(i + 1))
		writer.writerow(title)
		
		with open(fileIn) as read_file:
			
			csv_reader = csv.reader(read_file, delimiter=',')

			# initialize facial feature detection model
			detector = dlib.get_frontal_face_detector()
			predictor = dlib.shape_predictor("../data/face_weights.dat")
			cap = cv2.VideoCapture(videoPath)
			
			frame_num = 0
			frame_height = 120
			frame_width = 160
			row_count = 1
			count = 0
			middle_height = 0
			middle_width = 0
			totalRows = sum(1 for row in csv_reader)
			breakLoop = False
			read_file.seek(0)

			for i in csv_reader:
				if count == row_count:
					row = i
					break
				count += 1

			while True:
				_, frame = cap.read()
				gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)
				faces = detector(gray)
				top_y = 500
				bottom_y = 600
				left_x = 300
				right_x = 500
				for face in faces:
					x1 = face.left()
					y1 = face.top()
					x2 = face.right()
					y2 = face.bottom()
					landmarks = predictor(image=gray, box=face)
					for n in range(48, 61):
						x = landmarks.part(n).x
						y = landmarks.part(n).y
						middle_height = landmarks.part(57).y - landmarks.part(51).y
						padding_y = (frame_height - middle_height) // 2;
						if (frame_height - middle_height) % 2 == 1:
							top_y = landmarks.part(51).y - padding_y - 1
						else:
							top_y = landmarks.part(51).y - padding_y
						bottom_y = landmarks.part(57).y + padding_y

						middle_width = landmarks.part(64).x - landmarks.part(48).x

						padding_x = (frame_width - middle_width) // 2;
						if (frame_width - middle_width) % 2 == 1:
							left_x = landmarks.part(48).x - padding_x - 1
						else:
							left_x = landmarks.part(48).x - padding_x
						right_x = landmarks.part(64).x + padding_x
				
				if (middle_width + middle_height) / 2 <= 40:
					frame_num += 1
					continue

				frame = frame[top_y: bottom_y, left_x: right_x]

				if frame_num >= int(row[1]) and frame_num <= int(row[2]):
					
					dimensions = (64, 64)
					frame = cv2.resize(frame, dimensions, interpolation = cv2.INTER_AREA)
					frame = cv2.GaussianBlur(frame, (7,7), 0)
					
					array = []
					array.append(row[0])
					image = numpy.asarray(frame)
					grayscale_image = numpy.dot(image[...,:3], [0.299, 0.587, 0.144])
					grayscale_image = grayscale_image.astype(int)
					grayscale_image = grayscale_image.flatten()

					for pixel in grayscale_image:
						array.append(pixel)
					writer.writerow(array)

				elif frame_num > int(row[2]):
					
					row_count += 1
					if row_count == totalRows:
						break
					read_file.seek(0)
					csv_reader = csv.reader(read_file, delimiter=',')
					count = 0
					for i in csv_reader:
						if count == row_count:
							row = i
							break
						count += 1

					while int(row[1]) > int(row[2]):
						row_count += 1
						if row_count == totalRows:
							breakLoop = True
							break
						read_file.seek(0)
						csv_reader = csv.reader(read_file, delimiter=',')
						count = 0
						for i in csv_reader:
							if count == row_count:
								row = i
								break
							count += 1

					if breakLoop:
						break

					if frame_num >= int(row[1]) and frame_num <= int(row[2]):

						dimensions = (64, 64)
						frame = cv2.resize(frame, dimensions, interpolation = cv2.INTER_AREA)
						frame = cv2.GaussianBlur(frame, (7,7), 0)
						
						array = []
						array.append(row[0])
						image = numpy.asarray(frame)
						grayscale_image = numpy.dot(image[...,:3], [0.299, 0.587, 0.144])
						grayscale_image = grayscale_image.astype(int)
						grayscale_image = grayscale_image.flatten()
						
						for pixel in grayscale_image:
							array.append(pixel)
						writer.writerow(array)       

				frame_num += 1
				if cv2.waitKey(delay=1) == 27:
					break
			cap.release()
			cv2.destroyAllWindows()


if __name__ == '__main__':
	phonemes_and_timestamps_to_csv('../data/align_example.txt', "../data/phoneme_timestamps.csv")
	frames_per_phoneme("../data/phoneme_timestamps.csv", "../data/phoneme_framestamps.csv")
	crop_mouth('../data/phoneme_framestamps.csv', '../data/Test_Video.mp4', '../data/labeled_frames.csv')


	
