import cv2


video = 'data/Test_Video_1280x720_5_sec.mp4'
count = 0
vidcap = cv2.VideoCapture(video)
success,image = vidcap.read()
while success:
    vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))      # saves frame every 1000 milliseconds
    success,image = vidcap.read()
    print ('Read a new frame: ', success)
    cv2.imwrite( "Frames/frame%d.jpg" % count, image)     # save frame as JPEG file
    count = count + 1
