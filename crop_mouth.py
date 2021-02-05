import cv2
import dlib

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("/Users/allen/Desktop/Automated-Speech-Recognition/face_weights.dat")

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

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
        for n in range(57, 58):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(img=frame, center=(x, y), radius=3, color=(0, 255, 0), thickness=-1)

            top_y = landmarks.part(51).y
            bottom_y = landmarks.part(57).y
            left_x = landmarks.part(48).x
            right_x = landmarks.part(64).x

            print("highest_y", top_y)
            print("lowest_y", bottom_y)
            print("leftmost_x", left_x)
            print("rightmost_x", right_x)


     


    # show the image
    cv2.imshow(winname="Mouth", mat=frame)

    # Exit when escape is pressed
    if cv2.waitKey(delay=1) == 27:
        break

cap.release()
cv2.destroyAllWindows()