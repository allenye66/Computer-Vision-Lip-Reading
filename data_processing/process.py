import csv
import cv2
import dlib
import csv
import os.path
import math
def phonemes_and_timestamps_to_csv(dirname, fileIn):
	input_text = open(dirname)
	aligned_word_arr = []
	word_arr = []
	fail_words = 0
	line_num = 0
	for line in input_text:
		line_num += 1
		if '"alignedWord":' in line:
			aligned_word_arr.append(line_num)
		if '"word":' in line:
			word_arr.append(line_num)

	with open(dirname) as f:
	    text = f.readlines()
	text = [x.strip() for x in text] 
	current_time = 0
	header = ['phoneme', 'start', 'end']
	with open(fileIn, 'w') as g:
		writer = csv.writer(g)
		writer.writerow(header)
		for i in range(len(aligned_word_arr)):
			current_word_info = []
			for j in range(aligned_word_arr[i]-1, word_arr[i]):
				current_word_info.append(text[j])
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
			for k in range(len(durations)-1):
				start_times.append(round(start_times[k-1]+durations[k], 2))

			end_times = start_times[1:]
			end_times.append(round(start_times[-1]+durations[-1],2))
			print(phonemes)
			print(start_times)
			print(end_times)
			for j in range(len(phonemes)):
				row = [phonemes[j], start_times[j], end_times[j]]
				writer.writerow(row)



def frames_per_phoneme(fileIn, fileOut)
	fps = 24
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


def cropMouth(previousFileOut, videoPath)

	with open(previousFileOut) as csv_file:
	    csv_reader = csv.reader(csv_file, delimiter=',')
	    detector = dlib.get_frontal_face_detector()
	    predictor = dlib.shape_predictor("data/face_weights.dat")
	    cap = cv2.VideoCapture(videoPath)
	    frame_num = 0
	    frame_height = 120
	    frame_width = 160
	    row_count = 1
	    count = 0
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
	                cv2.circle(img=frame, center=(x, y), radius=3, color=(0, 255, 0), thickness=-1)
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
	        height = bottom_y - top_y
	        width = right_x - left_x
	        frame = frame[top_y: bottom_y, left_x: right_x]
	        print("Frame: "+str(frame_num)+" | "+row[1]+" - "+row[2]+" | "+str(frame_num >= int(row[1]) and frame_num <= int(row[2])))
	        if frame_num >= int(row[1]) and frame_num <= int(row[2]):
	            num = 0
	            pathName = "Frames/"+row[0]+"_"+str(num)+".jpg"
	            while os.path.exists(pathName):
	                num += 1
	                pathName = "Frames/"+row[0]+"_"+str(num)+".jpg"
	            cv2.imwrite(pathName, frame)
	        elif frame_num > int(row[2]):
	            row_count += 1
	            csv_file.seek(0)
	            csv_reader = csv.reader(csv_file, delimiter=',')
	            count = 0
	            for i in csv_reader:
	                if count == row_count:
	                    row = i
	                    break
	                count += 1
	            print("Frame: "+str(frame_num)+" | "+row[1]+" - "+row[2]+" | "+str(frame_num >= int(row[1]) and frame_num <= int(row[2])))
	            if frame_num >= int(row[1]) and frame_num <= int(row[2]):
	                num = 0
	                pathName = "Frames/"+row[0]+"_"+str(num)+".jpg"
	                while os.path.exists(pathName):
	                    num += 1
	                    pathName = "Frames/"+row[0]+"_"+str(num)+".jpg"
	                cv2.imwrite(pathName, frame)
	        cv2.imshow(winname="Mouth", mat=frame)
	        frame_num += 1
	        if cv2.waitKey(delay=1) == 27:
	            break
	    cap.release()
	    cv2.destroyAllWindows()
if __name__ == '__main__':

	phonemes_and_timestamps_to_csv('align_example.txt', "phoneme_timestamps.csv")
	frames_per_phoneme("phoneme_timestamps.csv", "phoneme_framestamps.csv")
	cropMouth('phoneme_framestamps.csv', 'Test_Video.mp4')


	
