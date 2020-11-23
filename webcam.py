import cv2, time
import numpy as np

faceCascade=cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier("/Users/allen/Desktop/Automated-Speech-Recognition/haarcascade_mouth.xml")
def regRecord():
	video = cv2.VideoCapture(0)
	a = 0
	while True:
		a = a + 1
		check, frame = video.read()
		faces = faceCascade.detectMultiScale(frame,1.1,4)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


		for (x,y,w,h) in faces:
			cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = frame[y:y+h, x:x+w]
			mouth = mouth_cascade.detectMultiScale(roi_gray)
			for (ex,ey,ew,eh) in mouth:
				cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

			#eyes = eye_cascade.detectMultiScale(roi_gray)
			#for (ex,ey,ew,eh) in eyes:
			#	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)


		cv2.imshow("Recording", frame)


		key = cv2.waitKey(1)

		if key == ord('q'):
			break
	print(a)

	video.release()


def grayRecord():
	video = cv2.VideoCapture(0)
	a = 0
	while True:
		a = a + 1
		check, frame = video.read()

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		cv2.imshow("Gray", gray)
		#cv2.imshow('Gray', gray)


		#cv2.waitKey(0)
		key = cv2.waitKey(1)

		if key == ord('q'):
			break
	print(a)

	video.release()
def edgeRecord():
	video = cv2.VideoCapture(0)
	a = 0
	while True:
		a = a + 1
		check, frame = video.read()
		edges = cv2.Canny(frame,50,200)
		cv2.imshow("Edges", edges)


		key = cv2.waitKey(1)

		if key == ord('q'):
			break
	print(a)
def contourRecord():
	video = cv2.VideoCapture(0)
	a = 0
	while True:
		a = a + 1
		check, frame = video.read()
		imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		ret, thresh = cv2.threshold(imgray, 127, 255, 0)
		contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		cv2.drawContours(frame, contours, -1, (0,255,0), 3)



		cv2.imshow("Contours", frame)

		#cv2.imshow('Gray', gray)


		#cv2.waitKey(0)
		key = cv2.waitKey(1)

		if key == ord('q'):
			break
	print(a)

	video.release()
if __name__ == '__main__':
	regRecord()
