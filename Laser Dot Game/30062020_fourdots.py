import imutils
import cv2
import sys
from imutils.video import WebcamVideoStream

webcam = WebcamVideoStream(src=0).start()
sys.path.append('.\\GazeTracking-master')
from gaze_tracking import GazeTracking

gaze = GazeTracking()

point = 0
left_eye = ()
right_eye = ()
text = "o"
coords_1 = (75, 75)
coords_2 = (300, 75)
coords_3 = (300, 300)
coords_4 = (75, 300)
coord_list = (coords_1, coords_2, coords_3, coords_4)

while True:
    frame = webcam.read()
    frame = cv2.flip(frame, 1)
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
    cv2.putText(frame, text, (75, 75), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 55, 231), 2)  # font for text
    cv2.putText(frame, text, (300, 75), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 55, 231), 2)  # font for text
    cv2.putText(frame, text, (300, 300), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 55, 231), 2)  # font for text
    cv2.putText(frame, text, (75, 300), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 55, 231), 2)  # font for text
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (260, 30), cv2.FONT_HERSHEY_DUPLEX, 0.4,
                (147, 147, 147), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (30, 30), cv2.FONT_HERSHEY_DUPLEX, 0.4,
                (147, 147, 147), 1)
    cv2.putText(frame, "Points: " + str(point), (30, 350), cv2.FONT_HERSHEY_DUPLEX, 0.6,
                (225, 225, 225), 1)
    for i in range(4):
        if (coord_list[i][0] - 50 <= left_eye[0] <= coord_list[i][0] + 50) or (
                coord_list[i][0] - 50 <= left_eye[1] <= coord_list[i][0] + 50) or (
                coord_list[i][1] - 50 <= right_eye[0] <= coord_list[i][1] + 50) or (
                coord_list[i][1] - 50 <= right_eye[1] <= coord_list[i][1] + 50):
            point += 1
            cv2.putText(frame, 'You\'re looking at Point ' + str(i + 1), (150, 350), cv2.FONT_HERSHEY_DUPLEX, 0.6,
                        (66, 185, 245),
                        2)  # font for text
            if i == 0:
                x=y=75
            elif i == 1:
                x=300
                y=75
            elif i == 2:
                x=y=300
            elif i == 3:
                x=75
                y=300
            cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 255, 31), 2)  # font for text
    # print('hello')
    cv2.imshow("Game Window", frame)
    if cv2.waitKey(1) == 27:  # ASCII for esc
        break

cv2.destroyAllWindows()
webcam.stop()