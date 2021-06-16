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


def compare_faces(pic_url, vid_url):
    # model = load_model('facenet_keras.h5')      # model for getting embeddings
    # slicing path string because folder reside in project directory
    pic_url = pic_url.rsplit("InVidett", 1)
    pic_url = pic_url[1][1:]
    # getting aligned face
    # pic_face= extract_align_face(pic_url)       #pic_face is aligned np array of face
    pic_face_array = np.array(Image.open(pic_url))
    pic_face = encodder.extract(pic_url)
    pic_face = pic_face[0]['box']
    x1, y1, width, height = pic_face
    x2, y2, = x1 + width, y1 + height
    pic_face = pic_face_array[y1:y2, x1:x2]
    # expanding dimensions for facenet
    pic_face = expand_dims(pic_face, axis=0)
    pic_embeddings = encodder.embeddings(np.array(pic_face))

    vid_url = vid_url.rsplit("InVidett", 1)
    vid_url = vid_url[1][1:]

    cap = cv2.VideoCapture(vid_url)
    countframes = 1

    # taking some variables for tracking purpose
    first_marked_frame, last_marked_frame, middle_frames, not_matched, outer_no_face = 0, 0, 0, 0, 0
    match = 0
    tracked_list = list()

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
        # detector = MTCNN()

        # saving all faces in result variable
        faces = encodder.extract(rgb_frame)
        # for face in faces:
        #     print(face['box'])
        #     x1, y1, width, height = face['box']
        #     # storing ending points in x2, y2
        #     print("extracted coordinates")
        #     x2, y2, = x1 + width, y1 + height
        #
        #     facen = img[y1:y2, x1:x2]
        #     print("cropped imaage")
        #     facen = expand_dims(facen, axis=0)
        #     embedding = embedder.embeddings(facen)

        # result = detector.detect_faces(rgb_frame)
        # print(faces)

        # if result get some faces
        if len(faces) > 0:
            print('found %s faces in frame: ' %len(faces), countframes)
            outer_no_face = 0
            frame_array = np.array(rgb_frame)
            # frame_array = asarray(rgb_frame)
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

                # frame_face = DeepFace.detectFace(frame_face, detector_backend='mtcnn')        #alignment postponed
                # frame_face = frame_face[:, :, ::-1]         # DeepFace detect internally using opeencv which return a BGR image so is that conversion

                # frame_face = DeepFace.detectFace()

                # to resiize, converting it PIL Image
                # frame_face = Image.fromarray(frame_face)
                # frame_face = frame_face.resize((160, 160))
                # with deepface above resizing generate exceptions or precisely conversion to PIL Image
                # thats why I will use open cv method to  resize it

                # frame_face = cv2.resize(frame_face, dsize=(160, 160), interpolation=cv2.INTER_CUBIC)      #no more needed resize as FaceNet will automatically resize it before embedding

                # back to array
                # frame_face = np.array(frame_face) #no more needed
                face_num += 1

                # changing logic to getting embedding and then calculate distance rather than using verify function
                # implementing deepface #no more neeced
                # recognised= df.verify(pic_face, frame_face, "Facenet")
                # print("Face number in current frame: ", face_num, "Above reuslts are for frame", countframes)
                frame_face_embeddings = get_embedding(frame_face)
                # getting distance through cosine
                distance = cosine(pic_embeddings, frame_face_embeddings)
                if distance >= 0.5:
                    recognised = False
                    print("picture input didn't matched for face number ", face_num, " in the frame ", countframes,
                          " where total faces in current frames are ", len(faces))
                else:
                    recognised = True
                    print("picture input matched for face number ", face_num, " in the frame ", countframes,
                          "when total faces in current frames are ", len(faces))
                    print("saving tracks for current frame ", countframes)

                if recognised == True:
                    match += 1
                    if match == 1:
                        first_marked_frame = countframes
                        print("First Match at frame: ", countframes)

                    not_matched = 0
                    print("Match is True for frame: ", first_marked_frame, "to ", countframes)
                    break

                else:
                    not_matched += 1
                    if not_matched == 6:
                        last_marked_frame = countframes - 30
                        print("Last Match at frame: ", countframes - 30)

                if last_marked_frame > 0:
                    tracked_list.append(first_marked_frame)
                    tracked_list.append(last_marked_frame)

                    match = 0
                    first_marked_frame = 0
                    last_marked_frame = 0

        else:
            outer_no_face += 1
            if outer_no_face == 4:
                if first_marked_frame > 0:
                    last_marked_frame = countframes - 20
                    tracked_list.append(first_marked_frame)
                    tracked_list.append(last_marked_frame)

                    match = 0
                    first_marked_frame = 0
                    last_marked_frame = 0
                    print("Last Matched frame: ", countframes - 20)

                # append in face list
                # faces_list.append(frame_face)

        print("Total frames processed: ", countframes)
        # just for test purpose limiting frames
        # if countframes >= 130:
        #     break

    # for last tracking duration
    if first_marked_frame > 0:
        last_marked_frame = countframes
        tracked_list.append(first_marked_frame)
        tracked_list.append(last_marked_frame)
        print("Last Matched frame: ", countframes)


    # saving faces list into npz
    # savez("video_faces.npz", faces_list)

    # releasing video and destroying windows
    cap.release()
    return tracked_list

# img= extract_align_face("pic_input/2021-05-21-093418.jpg")
# # img= fromarray(img)
# plt.imshow(img)