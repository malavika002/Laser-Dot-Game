import imutils
import cv2
import sys
from imutils.video import WebcamVideoStream
import random as rn
webcam = WebcamVideoStream(src=0).start()
sys.path.append('.\\GazeTracking-master')
from gaze_tracking import GazeTracking

gaze = GazeTracking()

x = rn.randint(0, 480)
y = rn.randint(0, 360)
level_ct=1
game_point=0
left_eye = ()
right_eye = ()
text = "o"

while level_ct<=100:
    coord_list = (x, y)
    frame = webcam.read()
    frame = cv2.flip(frame,1)
    frame = imutils.resize(frame, width=480, height=360)
    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)
    frame = gaze.annotated_frame()
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    l_p = str(left_pupil)
    r_p = str(right_pupil)
    if l_p != 'None':
        l_p = l_p.replace('(', '')
        l_p = l_p.replace(')', '')
        r_p = r_p.replace('(', '')
        r_p = r_p.replace(')', '')
        left_eye = tuple(map(int, l_p.split(', ')))
        right_eye = tuple(map(int, r_p.split(', ')))
        # print('left_eye is: ', left_eye)
    else:
        continue

    cv2.putText(frame, text, (x,y), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 55, 231), 2)  # font for text
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (260, 30), cv2.FONT_HERSHEY_DUPLEX, 0.4,
                (147, 147, 147), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (30, 30), cv2.FONT_HERSHEY_DUPLEX, 0.4,
                (147, 147, 147), 1)
    cv2.putText(frame, "Points: " + str(game_point), (30, 350), cv2.FONT_HERSHEY_DUPLEX, 0.6,
                (225, 225, 225), 1)
    cv2.putText(frame, 'You\'re on level: ' + str(level_ct), (200, 350), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0),
                2)  # font for text
    cv2.putText(frame, "Point is at: " + str(coord_list), (30, 50), cv2.FONT_HERSHEY_DUPLEX, 0.4,
                (225, 0, 231), 1)
    if (coord_list[0]-25<=left_eye[0]<=coord_list[0]+25) or (coord_list[1]-25<=left_eye[1]<=coord_list[1]+25) or (coord_list[0]-25<=right_eye[0]<=coord_list[0]+25) or (coord_list[1]-25<=right_eye[1]<=coord_list[1]+25):
       game_point+=1
       cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 255, 0), 2)  # font for text
    if game_point%17==1:
        level_ct+=1
        if game_point%level_ct==0:
            x = rn.randint(0, 480)
            y = rn.randint(30, 250)
    if level_ct==15:
        cv2.waitKey(100)
        cv2.putText(frame, 'You\'ve Won! ', (100, 170), cv2.FONT_HERSHEY_DUPLEX, 1.6, (168, 50, 139),
                    2)  # font for text

    cv2.imshow("Game Window", frame)
    if cv2.waitKey(1) == 27:  # ASCII for esc
        break

cv2.destroyAllWindows()
webcam.stop()