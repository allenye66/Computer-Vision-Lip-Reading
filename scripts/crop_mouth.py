import cv2
import dlib
import csv
import os.path
import numpy
import sys

phoneme_framestamps = '../data/phoneme_framestamps.csv'
video = '../data/Test_Video.mp4'
fileOut = '../data/labeled_frames.csv'
numpy.set_printoptions(threshold=sys.maxsize)


with open(fileOut, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Frame", "Phoneme", "Image"])

    with open(phoneme_framestamps) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("../data/face_weights.dat")

        # cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture(video)
        frame_num = 0
        frame_height = 120
        frame_width = 160
        row_count = 1
        middle_height = 0
        middle_width = 0
        # row = [rows for idx, rows in enumerate(csv_reader) if idx == 1][0]
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

            #HAVE TO SET TO NON ZERO CONSTANTS IN THE BEGINNING JUST IN CASE THE ALGORITHM CANT FIND MOUTH IMMEDIATELY
            top_y = 500
            bottom_y = 600
            left_x = 300
            right_x = 500

            for face in faces:
                x1 = face.left()  # left point
                y1 = face.top()  # top point
                x2 = face.right()  # right point
                y2 = face.bottom()  # bottom point

               
                landmarks = predictor(image=gray, box=face)

                # Loop through all the points (0-68 for all features)
                #top: 51
                #bottom: 57
                #left: 48
                #right: 64
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
                    
                    
            # print("top_y", top_y)
            # print("bottom_y", bottom_y)
            # print("left_x", left_x)
            # print("right_x", right_x)
            height = bottom_y - top_y
            width = right_x - left_x
            # print('Frame: ' + str(width) + ' x ' + str(height))
            if (middle_width + middle_height) / 2 <= 40:
                continue


            #upper_left = (left_x - border, top_y - border)
            #bottom_right = (right_x + 50, bottom_y + 50)
            #height = border*2 + abs(top_y -bottom_y)
            #width = border*2 + abs(left_x -right_x)

            # show the image
            
            #frame = frame[upper_left[1]:upper_left[1]+height, upper_left[0]:upper_left[0]+width]
            frame = frame[top_y: bottom_y, left_x: right_x]
            
            print("Frame: "+str(frame_num)+" | "+row[1]+" - "+row[2]+" | "+str(frame_num >= int(row[1]) and frame_num <= int(row[2])))
            if frame_num >= int(row[1]) and frame_num <= int(row[2]):
                num = 0
                pathName = "../Frames/"+row[0]+"_"+str(num)+".jpg"
                while os.path.exists(pathName):
                    num += 1
                    pathName = "../Frames/"+row[0]+"_"+str(num)+".jpg"
                
                cv2.imwrite(pathName, frame)    # save frame
                # image = numpy.asarray(frame)
                # print(image.shape)
                # writer.writerow([frame_num,row[0],image])
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
                    pathName = "../Frames/"+row[0]+"_"+str(num)+".jpg"
                    while os.path.exists(pathName):
                        num += 1
                        pathName = "../Frames/"+row[0]+"_"+str(num)+".jpg"
                    cv2.imwrite(pathName, frame)    # save frame
                    # image = numpy.asarray(frame)
                    # print(image.shape)
                    # writer.writerow([frame_num,row[0],image])
                
            
            cv2.imshow(winname="Mouth", mat=frame)

            frame_num += 1

            # Exit when escape is pressed
            if cv2.waitKey(delay=1) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()