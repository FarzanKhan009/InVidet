#History:
#tested many thing in last couple of days
#its been hard to to generalise this module for face input
#and video input, now while testing detection in video file
#I altered many logics, I am going to change logic in this
#too putting an end to efforts at generalizing only module
#for pic and video input, later I may reverse this decison
import cv2
import numpy as np
from PIL import Image
from mtcnn_cv2 import MTCNN
from numpy import asarray, savez
import matplotlib.pyplot as plt


def create_npz_faces(url="vid_input/video.webm"):
    cap = cv2.VideoCapture(url)
    countframes = 0
    faces_list= list()
    while True:
        # Grab a single frame of video
        try:
            ret, frame = cap.read()
            countframes += 1

        except:
            print("URL/selection for the video file is not valid:", url)
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

        #if result get some faces
        if len(result) > 0:
            frame_array= np.array(rgb_frame)
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

                #to resiize, converting it PIL Image
                frame_face= Image.fromarray(frame_face)
                frame_face= frame_face.resize((160,160))
                #back to array
                frame_face= asarray(frame_face)


                #append in face list
                faces_list.append(frame_face)


        print(countframes)
        #just for test purpose limiting frames
        if countframes >=130:
            break


    #saving faces list into npz
    savez("video_faces.npz", faces_list)


    # releasing video and destroying windows
    cap.release()
    return


def plot_from_npz():
    faces_np_name= "video_faces.npz"
    faces= np.load(faces_np_name)['arr_0']
    for face_arr in faces:
        face= Image.fromarray(face_arr)
        plt.imshow(face)
    print("outer")
    plt.show()


create_npz_faces()
# plot_from_npz()