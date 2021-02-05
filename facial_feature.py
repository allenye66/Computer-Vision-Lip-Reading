import cv2
import dlib
import math
import unittest
import numpy as np
import urllib.request

from scipy.spatial import distance
from matplotlib import pyplot as plt
frontalface_detector = dlib.get_frontal_face_detector()
img = cv2.imread('/Users/allen/Desktop/Automated-Speech-Recognition/download.jpg')

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

#detect_face(img)
image,landmarks= get_landmarks(img) #url

#Plot the Facial Landmarks on the face
if landmarks:
  image_landmarks(image,landmarks)
else:
  print ("No Landmarks Detected")
