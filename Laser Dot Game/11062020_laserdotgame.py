import imutils
import cv2
import sys
import random as rn
webcam = cv2.VideoCapture(0)
sys.path.append('.\\GazeTracking-master')
from gaze_tracking import GazeTracking

gaze = GazeTracking()
x = rn.randint(0, 480)
y = rn.randint(0, 360)
_,frame = webcam.read()
point=0
text = "o"
while True:
    coord_list = (str(x),str(y))
    text = "o"
    frame = imutils.resize(frame, width=480, height=360)
    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)
    frame = gaze.annotated_frame()
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 255, 231), 2)  # font for text
    cv2.putText(frame, "Points: " + str(point), (30, 30), cv2.FONT_HERSHEY_DUPLEX, 0.6,
                (225, 225, 225), 1)

    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (260, 30), cv2.FONT_HERSHEY_DUPLEX, 0.6,
                (147, 147, 147), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (260, 65), cv2.FONT_HERSHEY_DUPLEX, 0.6,
                (147, 147, 147), 1)
    cv2.putText(frame, "Point is at: " + str(coord_list), (30, 50), cv2.FONT_HERSHEY_DUPLEX, 0.6,
                (225, 0, 231), 1)

    if str(left_pupil)==coord_list or str(right_pupil)==coord_list:
        point+=1
        x = rn.randint(0, 480)
        y = rn.randint(0, 360)
    cv2.imshow("Game Window", frame)  # shows back to the window
    if cv2.waitKey(1) == 27:  # ASCII for esc
        break
    # We get a new frame from the webcam
    _, frame = webcam.read()

