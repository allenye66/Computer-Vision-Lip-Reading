import cv2
import dlib

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("/Users/allen/Desktop/Automated-Speech-Recognition/face_weights.dat")

cap = cv2.VideoCapture(0)

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
            
            padding_y = 5
            padding_x = 20
            top_y = landmarks.part(51).y  - padding_y
            bottom_y = landmarks.part(57).y  + padding_y
            left_x = landmarks.part(48).x - padding_x
            right_x = landmarks.part(64).x + padding_x



    print("top_y", top_y)
    print("bottom_y", bottom_y)
    print("left_x", left_x)
    print("right_x", right_x)



    #upper_left = (left_x - border, top_y - border)
    #bottom_right = (right_x + 50, bottom_y + 50)
    #height = border*2 + abs(top_y -bottom_y)
    #width = border*2 + abs(left_x -right_x)

    # show the image
    
    #frame = frame[upper_left[1]:upper_left[1]+height, upper_left[0]:upper_left[0]+width]
    frame = frame[top_y: bottom_y, left_x: right_x]
    cv2.imshow(winname="Mouth", mat=frame)

    # Exit when escape is pressed
    if cv2.waitKey(delay=1) == 27:
        break

cap.release()
cv2.destroyAllWindows()