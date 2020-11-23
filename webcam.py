import cv2
import dlib
import math
import unittest
import numpy as np
import urllib.request

from scipy.spatial import distance
from matplotlib import pyplot as plt
frontalface_detector = dlib.get_frontal_face_detector()

def rect_to_bb(rect):

	x = rect.left()
	y = rect.top()
	w = rect.right() - x
	h = rect.bottom() - y
	return (x, y, w, h)

def detect_face(img):
	rects = frontalface_detector(img, 1)

	for (i, rect) in enumerate(rects):
		(x, y, w, h) = rect_to_bb(rect)
		cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

	plt.imshow(img, interpolation='nearest')
	plt.axis('off')
	plt.show()

def get_landmarks(image):
	landmark_predictor = dlib.shape_predictor('/Users/allen/Desktop/Automated-Speech-Recognition/face_weights.dat')

	faces = frontalface_detector(image, 1)
	if len(faces):
		landmarks = [(p.x, p.y) for p in landmark_predictor(image, faces[0]).parts()]
	else:
		return None,None
	return image,landmarks

def image_landmarks(image,face_landmarks):
  radius = -1
  circle_thickness = 5
  image_copy = image.copy()
  for (x, y) in face_landmarks:
  	cv2.circle(image_copy, (x, y), circle_thickness, (255,0,0), radius)
	
  plt.imshow(image_copy, interpolation='nearest')
  plt.axis('off')
  plt.show()

def regRecord():
	video = cv2.VideoCapture(0)
	a = 0
	while True:
		a = a + 1
		check, frame = video.read()
		
		image,landmarks= get_landmarks(frame) #url


		cv2.imshow("Recording", frame)
		if landmarks:
  			image_landmarks(image,landmarks)



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
