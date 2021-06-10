# this module is istegrated approah for detection in video for each
# frame at the same time extracting and comparing so that less burdon
# on RAM also no need to store them in directory as Images or npz files
import numpy as np
from PIL import Image
from cv2 import cv2
from mtcnn_cv2 import MTCNN
from numpy import asarray

import rec_by_deepface as df


def compare_faces(pic_face, vid_url):
    vid_url = vid_url.rsplit("InVidett", 1)
    vid_url = vid_url[1][1:]

    cap = cv2.VideoCapture(vid_url)
    countframes = 1

    # taking some variables for tracking purpose
    first_marked_frame, last_marked_frame, middle_frames, not_matched, outer_no_face= 0,0,0,0,0
    match= 0
    tracked_list= list()


    # faces_list = list()
    while True:
        # Grab a single frame of video
        try:
            ret, frame = cap.read()
            countframes += 1

        except:
            print("URL/selection for the video file is not valid:", vid_url)
            break

        # below if conditional logic is to boost up the speed
        # reducing frames rate 6 fps actual was 30fps
        if countframes % 5 != 0:
            continue

        # Convert the image from BGR color(which OpenCV uses) to RGB
        # RGB is preferred color while detection faces
        try:
            rgb_frame = frame[:, :, ::-1]
        except:
            print("video file has no more frames, total frames= ", countframes)
            break

        # loading detector from MTCNN
        detector = MTCNN()

        # saving all faces in result variable
        result = detector.detect_faces(rgb_frame)
        print(result)

        # if result get some faces
        if len(result) > 0:
            frame_array = np.array(rgb_frame)
            # frame_array = asarray(rgb_frame)

            # taking variable face_num; to iterate in loop; for detecting multiple faces in single frame
            face_num = 0
            for face in result:
                # read the documentation of cv2.rectangle()
                # starting point coordinates of face are being stored in x1, y1
                x1, y1, width, height = result[face_num]['box']
                # storing ending points in x2, y2
                x2, y2, = x1 + width, y1 + height

                # extracting this face from frame_array
                frame_face = frame_array[y1:y2, x1:x2]

                # to resiize, converting it PIL Image
                frame_face = Image.fromarray(frame_face)
                frame_face = frame_face.resize((160, 160))
                # back to array
                frame_face = asarray(frame_face)
                face_num += 1


                # implementing deepface
                recognised= df.verify(pic_face, frame_face, "Facenet")
                # print("Face number in current frame: ", face_num, "Above reuslts are for frame", countframes)

                if recognised== True:
                    match+= 1
                    if match == 1:
                        first_marked_frame= countframes
                        print("First Match at frame: ", countframes)

                    not_matched=0
                    print("True for frames: ", first_marked_frame, "to ", countframes)
                    break

                else:
                    not_matched += 1
                    if not_matched ==6:
                        last_marked_frame= countframes- 30
                        print("Last Match at frame: ", countframes)

                if last_marked_frame >0:
                    tracked_list.append(first_marked_frame)
                    tracked_list.append(last_marked_frame)

                    match=0
                    first_marked_frame=0
                    last_marked_frame=0

        else:
            outer_no_face+=1





                # append in face list
                # faces_list.append(frame_face)

        if outer_no_face == 60:
            if first_marked_frame >=0:
                last_marked_frame = countframes - 60
                tracked_list.append(first_marked_frame)
                tracked_list.append(last_marked_frame)

                match=0
                first_marked_frame=0
                last_marked_frame=0
                print("Last Mathed frame: ", countframes)

        print("Total frames processed: ", countframes)
        # just for test purpose limiting frames
        # if countframes >= 130:
        #     break

    # saving faces list into npz
    # savez("video_faces.npz", faces_list)

    # releasing video and destroying windows
    cap.release()
    return

