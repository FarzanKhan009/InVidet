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


def create_npz_faces():
    cap = cv2.VideoCapture("vid_input/multi-face.mp4")
    countframes = 0
    faces_list= list()
    while True:
        # Grab a single frame of video
        try:
            ret, frame = cap.read()
            countframes += 1

        except:
            print("End of frames")
            break

        # below if conditional logic is to boost up the speed
        # reducing frames rate 6 fps actual was 30fps
        if countframes % 5 != 0:
            continue

        # Convert the image from BGR color(which OpenCV uses) to RGB
        # RGB is preferred color while detection faces
        rgb_frame = frame[:, :, ::-1]

        # loading detector from MTCNN
        detector = MTCNN()

        # saving all faces in result variable
        result = detector.detect_faces(rgb_frame)

        # if only one face in the frames
        print(result)

        if len(result) > 0:
            # to work with deep face
            frame_array= np.array(rgb_frame)
#            frame_array = asarray(rgb_frame)

            # taking variable face_num; to iterate in loop; for detecting multiple faces in single frame
            face_num = 0
            for face in result:
                # if confused read the documentation of cv2.rectangle() it would help a lot

                # starting point of the face is stored in x1, y1 as tupple i.e. (x1,y1)
                x1, y1, width, height = result[face_num]['box']
                # storing ending points in x2, y2
                x2, y2, = x1 + width, y1 + height

                # appeared in frames to a directory; to work with deepface
                # creating image from image array to store in directory video_frames
                frame_face = frame_array[y1:y2, x1:x2]
                #            size=(160,160)
                #            frame_face = frame_face.resize(size)

                frame_face= Image.fromarray(frame_face)
                frame_face= frame_face.resize((160,160))
                frame_face= asarray(frame_face)


                #I will change logic here
                #I will try saving in npz numpy zip
                faces_list.append(frame_face)


                # setting a trackable name
#                face_name = f'{countframes}{"-"}{face_num}'
#                frame_path = "extracted_faces_video_frames/" + face_name + ".jpg"
                # saving single face of frame in directory
#                cv2.imwrite(frame_path, frame_face[:, :, ::-1])

                # cv2.rectangle(start, end, color(RGB), (pixel of drawn line))
                # drawing rectangle araound the face
#                cv2.rectangle(frame, (x1, y1),
#                              (x2, y2), (0, 155, 255), 2)
#                face_num += 1

        # Display the resulting frames video
#        cv2.imshow('Video', frame)
        print(countframes)
        if countframes >=130:
            break

        # Wait for Enter key to stop
        if cv2.waitKey(25) == 13:
            break

    #saving faces list into npz
    savez("video_faces.npz", faces_list)


    # releasing video and destroying windows
    cap.release()
    cv2.destroyAllWindows()
    return


def plot_from_npz():
    faces_np_name= "video_faces.npz"
    faces= np.load(faces_np_name)
    for face_arr in faces:
        face= Image.fromarray(face_arr)
       # plt.imshow(face_arr)
    #plt.show()


create_npz_faces()
plot_from_npz()