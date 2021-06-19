# this module is integrated approach for detection in video for each
# frame at the same time extracting and comparing so that less burden
# on RAM also no need to store them in directory as Images or npz files
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from PIL.Image import fromarray
from cv2 import cv2
from keras.backend import expand_dims
from mtcnn_cv2 import MTCNN
from numpy import asarray
# from keras.models import load_model     # to get FaceNet Embedding model
from deepface import DeepFace
from keras_facenet import FaceNet  # it will load model, without error
from scipy.spatial.distance import cosine

import rec_by_deepface as df

# seeting model encodder to global
encodder = FaceNet()


def extract_align_face(img):  # it return align face
    result = DeepFace.detectFace(img)
    # print(result)
    return result


def get_embedding(face):
    # face = expand_dims(face, axis=0)
    embeddings = encodder.embeddings(np.array(face))
    return embeddings


def compare_faces(pic_url, vid_url, fps, threshold, v_fps, person_name, v_out, v_show, video_file):
    # setting divisible by using v_fps to fast or slow the process i.e. how much frames to skip
    # frame_array= (10,10,255)
    # out=0
    print("[INFO] TensorFlow Loaded")
    print("[INFO] Module Compare Faces Received Call")
    divisible=0
    tolerance=4

    # checking it is a cam stream, if it is, setting fps by self, not relying on cv2 to get fps from video file or else it raised exception modulo by zero
    #bug fix 1.4
    if video_file == False:
        fps=30
    if v_fps==1:
        divisible =  fps
        tolerance = 2
    if v_fps==2:
        tolerance = 3
        divisible = fps/2
    if v_fps==3:
        tolerance = 3
        divisible = fps/3
    if v_fps==4:
        tolerance = 3
        divisible = fps/4
    print("[INFO] Tolerance set to ", tolerance, " for missing frames")
    print("[INFO] Calculating divisible based on tolerance...")
    print("[INFO] Divisible set to", divisible)

    # slicing path string because folder reside in project directory
    pic_url = pic_url.rsplit("InVidett", 1)
    pic_url = pic_url[1][1:]
    # getting aligned face
    # pic_face= extract_align_face(pic_url)       #pic_face is aligned np array of face
    # print(pic_url)
    pic_face_array = np.array(Image.open(pic_url))
    pic_face = encodder.extract(pic_url)
    pic_face = pic_face[0]['box']
    x1, y1, width, height = pic_face
    x2, y2, = x1 + width, y1 + height
    pic_face = pic_face_array[y1:y2, x1:x2]
    # expanding dimensions for facenet
    pic_face = expand_dims(pic_face, axis=0)
    pic_embeddings = encodder.embeddings(np.array(pic_face))



    total_frames= 99

    # initializing to count tota frames
    # initializing list() to track frames
    tracked_list = list()
    # making sure video is readable

    if video_file:
        try:
            vid_url = vid_url.rsplit("InVidett", 1)
            vid_url = vid_url[1][1:]
            cap = cv2.VideoCapture(vid_url)
            print("[INFO] Video file is successfully loaded")

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        except:
            print("[ERROR] Video is unable to load, check path")
            tracked_list= ["ERROR"]
            return tracked_list
    else:
        try:
            cap = cv2.VideoCapture(0)
            print("[INFO] Video file is successfully loaded")
        except:
            print("[ERROR] Video is unable to load, check path")
            tracked_list = ["ERROR"]
            return tracked_list


    # if only video write option is true; then write
    if v_out:
        print("[INFO] Video write option is set TRUE, initializing")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('pic_input/output.avi', fourcc, v_fps, (640, 480))
        print("[INFO] Output video path is set to pic_input/output.avi")

    # initializing frame counts
    countframes = 0

    # taking some variables for tracking purpose
    first_marked_frame, last_marked_frame, not_matched, outer_no_face, match= 0, 0, 0, 0, 0
    # match = 0


    # faces_list = list()
    while True:
        try:
            ret, frame = cap.read()
            countframes += 1
        except:
            print("[WARN] URL/selection for the video file is not valid:", vid_url)
            print("[WARN] Could not more frames")
            break

        # below if conditional logic is to boost up the speed
        # taking frame rate to verify from user, implemented, divisible is obtained from user choice
        if countframes % int(divisible) != 0:
            continue

        # Convert the image from BGR color(which OpenCV uses) to RGB
        # RGB is preferred color while detection faces
        try:
            rgb_frame = frame[:, :, ::-1]
            frame_array = np.array(rgb_frame)
        except:
            # bug fix 1.3
            print("[ERROR] Video file is corrupted or has no more frames, total frames= ", countframes)
            break

        # loading detector from MTCNN
        # detector = MTCNN()

        # saving all faces in faces
        faces = encodder.extract(rgb_frame)

        # if result get some faces
        if len(faces) > 0:
            print('[INFO] Found %s faces in frame: ' %len(faces), countframes)

            # initializing to check frames with no faces
            outer_no_face = 0

            # taking variable face_num; to iterate in loop; for detecting multiple faces in single frame
            face_num = 0

            for face in faces:
                # read the documentation of cv2.rectangle()
                # starting point coordinates of face are being stored in x1, y1
                x1, y1, width, height = faces[face_num]['box']

                # storing ending points in x2, y2
                x2, y2, = x1 + width, y1 + height

                # extracting this face from frame_array
                frame_face = frame_array[y1:y2, x1:x2]

                # expanding dimensions to normalize it for facenet
                frame_face = expand_dims(frame_face, axis=0)

                # back to array
                # frame_face = np.array(frame_face) #no more needed

                # increasing face number to extract the next face 'BOX' in current frame
                face_num += 1

                # bug fix
                # at testing while getting embedding it raised exception, says in resize function of FaceNet
                try:
                    frame_face_embeddings = get_embedding(frame_face)
                except:
                    print("[WARN] Exception raised")
                    print("[WARN] Could not get embedding for frame ", countframes, "/",total_frames)
                    continue

                # getting distance through cosine
                distance = cosine(pic_embeddings, frame_face_embeddings)

                # used threshold provided by user from GUI module
                if distance >= threshold:
                    recognised = False
                    print("[INFO] Match is False for face", face_num,"/",len(faces), " in the frame", countframes,"/",total_frames)
                else:
                    recognised = True
                    print("[INFO] Match is True for face", face_num,"/",len(faces), " in the frame", countframes,"/",total_frames)
                    print("[INFO] Saving tracks for current frame", countframes)
                    print("[INFO]", person_name, "found with the distance", str(distance)[0:5])

                # logic when face is recognised
                if recognised == True:
                    match += 1

                    # only show frames or video if it set true
                    if v_show:
                        text = "["+person_name+"]" + " , [DISTANCE] " + str(distance)[0:4]
                        # "y" show name upper side of bounding box if there is space if no space left show towards donside
                        y = y1 - 10 if y1 - 10 > 10 else y1 + 10
                        cv2.rectangle(frame_array, (x1, y1), (x2, y2), (155, 25, 25), 2)
                        cv2.putText(frame_array, text, (x1, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (155, 25, 25), 2)


                    # marking first frame
                    if match == 1:
                        first_marked_frame = countframes
                        print("[INFO] First Match at frame: ", countframes,"/",total_frames)

                    not_matched = 0
                    print("[INFO] Match is True for frame: ", first_marked_frame, " to ", countframes)
                    break

                else:
                    # logic when face is not matched, tolerance tells how much to tolerate this behaviour
                    not_matched += 1
                    # adding length of faces too, because if there are too many faces tolerate will fail, if alone, Doubt not tested yet
                    if not_matched == (tolerance*len(faces)):
                        if first_marked_frame > 0:
                            last_marked_frame = int(countframes - (tolerance * divisible))

                            tracked_list.append(first_marked_frame)
                            tracked_list.append(last_marked_frame)

                            first_marked_frame = 0
                            last_marked_frame = 0
                            match= 0
                            print("[INFO] Last Match at frame: ", countframes - (tolerance* divisible))


        else:
            # logic when no face is found in current frame
            outer_no_face += 1
            if outer_no_face == tolerance:
                if first_marked_frame > 0:
                    last_marked_frame = int(countframes - (tolerance * divisible))
                    tracked_list.append(first_marked_frame)
                    tracked_list.append(last_marked_frame)

                    match = 0
                    first_marked_frame = 0
                    last_marked_frame = 0
                    print("[INFO] Last Matched frame: ", countframes - (tolerance* divisible), "/", total_frames)

                # append in face list
                # faces_list.append(frame_face)

        print("[INFO] Total frames processed: ", countframes, "/", total_frames)
        # just for test purpose limiting frames, it was at initial testing
        # if countframes >= 130:
        #     break

        # only write current frame if v_out is true
        if v_out:
            print("[INFO] Writing frame ", countframes, "/", total_frames, " in output video")
            out.write(frame_array[:, :, ::-1])
            # cv2.waitKey(1)
            # if cv2.waitKey(0) & 0xFF == ord('q'):
            #     break

        # only show if it sets true
        if v_show:
            print("[INFO] Showing frame ", countframes,"/", total_frames)
            cv2.imshow("InVidet", frame_array[:, :, ::-1])
            # ideal is waitkey(0), but (1) is working for me
            # cv2.waitKey(1)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    # for last verified  frame, if it is not tracked
    if first_marked_frame > 0:
        last_marked_frame = countframes
        tracked_list.append(first_marked_frame)
        tracked_list.append(last_marked_frame)
        print("[INFO] Final Matched frame: ", countframes,"/", total_frames)
        print("[INFO] Returning tracked list back to GUI")


    # releasing video and destroying windows
    cap.release()
    # releasing out if initialized
    if v_out:
        out.release()
    cv2.destroyAllWindows()
    return tracked_list

# img= extract_align_face("pic_input/2021-05-21-093418.jpg")
# # img= fromarray(img)
# plt.imshow(img)