import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from PIL.Image import fromarray
from deepface import DeepFace
from facenet_pytorch.models.inception_resnet_v1 import load_weights
# from keras.backend import expand_dims
# from keras.models import load_model
from mtcnn_cv2 import MTCNN
import tensorflow as tf
from keras_facenet import FaceNet

# from deepface import DeepFace.face_align
# model = load_model('facenet_keras.h5')
# model = load_model()
# keras_model = tf.keras.models.load_model( 'facenet_keras.h5' )
from numpy import expand_dims
from scipy.spatial.distance import cosine

encoder= FaceNet()
def get_embedding(face):
    print("recv call on embed")
    face= expand_dims(face, axis=0)
    embeddings = encoder.embeddings(face)
    print("sending back embed")
    return embeddings

path= "pic_input/multiface.jpeg"
# path1= "pic_input/single-face-pic-input.jpg"
path= cv2.imread(path)[:,:, ::-1]
# path1= cv2.imread(path1)[:,:, ::-1]
detector = MTCNN()
result = detector.detect_faces(path)
# result1= detector.detect_faces(path1)
print(result)
# print(result1)
# model= DeepFace.Facenet.loadModel("facenet_keras.h5")
rgb_faces= list()
mtcn_face= list()
score, score1= 0,0
# model= DeepFace.Facenet.loadModel("https://drive.google.com/drive/folders/12aMYASGCKvDdkygSv1yQq8ns03AStDO_"")
# if result get some faces
if len(result) > 0:
    outer_no_face = 0
    frame_array = np.array(path)
    # frame_array1= np.array(path1)
    # frame_array = asarray(rgb_frame)

    # taking variable face_num; to iterate in loop; for detecting multiple faces in single frame
    face_num = 0
    for face in result:
        # read the documentation of cv2.rectangle()
        # starting point coordinates of face are being stored in x1, y1
        x1, y1, width, height = result[face_num]['box']
        # storing ending points in x2, y2
        x2, y2, = x1 + width +10, y1 + height +10
        x1,y1= x1-10,y1-10

        # extracting this face from frame_array
        frame_face = frame_array[y1:y2, x1:x2]



        mtcn_face.append(frame_face)
        try:
            frame_face = DeepFace.detectFace(frame_face, detector_backend='mtcnn')
        except:
            print("some exception occure")
            face_num+= 1
            continue
        print("face no: %s" % face_num)
        # except:
        #     print("Face is not detected by deepface")
        rgb_face = frame_face[:, :, ::-1]
        # rgb_face = cv2.resize(rgb_face, dsize=(160, 160), interpolation=cv2.INTER_CUBIC)
        # print(rgb_face.shape, type(rgb_face))
        # plt.figure("face_num+1")
        # plt.imshow(rgb_face)

        # print(rgb_face)
        if face_num==0:
            plt.figure("0")
            plt.imshow(rgb_face)
            score = get_embedding(mtcn_face[0])
        elif face_num==1:
            plt.figure("1")
            plt.imshow(rgb_face)
            score1 = get_embedding(mtcn_face[1])
        # rgb_faces.append()
        face_num += 1


plt.show()
# print(frame_face)
# print(get_embedding(frame_face))
# print(rgb_face.shape, type(rgb_face))
# plt.figure("1")
# plt.imshow(rgb_face)

# rgb_face= fromarray(rgb_face).resize((160,160))
# i=0
# for i in range(len(mtcn_face)):
#     print( "length mtcnn",len(mtcn_face))
#     plt.figure("mtcnn no %s" % i)
#     plt.imshow(mtcn_face[i])
#     try:
#         print("length of rgb", len(rgb_faces))
#         plt.figure("figure no %s" % i)
#         plt.imshow(rgb_faces[i])
#     except:
#         print("plt lack in deep face")
#         continue
#     # plt.show()
#     i+=1
# # plt.figure("2")
# # plt.imshow(rgb_face1)
# plt.show()

#implement embed
# mt= cv2.resize(mtcn_face[0], dsize=(160, 160), interpolation=cv2.INTER_CUBIC)
# print(get_embedding())
# print(rgb_faces[1] ,"started embed")
# curface= rgb_faces[1]
#
# print(curface, "face",curface.shape)
# curface = curface.astype('float32')
# # standardize pixel values across channels (global)
# mean, std = curface.mean(), curface.std()
# curface = (curface - mean) / std
# curface = expand_dims(curface, axis=0)
# print("dimension expaded")
# print(curface, "face",curface.shape)
#
# curfacemb= get_embedding(curface)
# print("embed on face", curfacemb)
# # print("no embed completed")
# print("calculating cosine distance")
# curface1= rgb_faces[3]
#
# curface1 = curface1.astype('float32')
# mean, std = curface1.mean(), curface1.std()
# curface1 = (curface1 - mean) / std
# curface1 = expand_dims(curface1, axis=0)
# # curface1= expand_dims(curface1, axis=0)
# curface1mb= get_embedding(curface1)
# print("second input embedding: ", curface1mb)

# score= cosine(curfacemb, curface1mb)

# if score <=0.5:
#     print("matched", score)
# else:
#     print("not matched", score)
#
# score1= cosine(curfacemb, curfacemb)
# if score1 <=0.5:
#     print("matched", score1)
# else:
#     print("not matched", score1)

# i=0
# print("length: ", len(rgb_faces))
# for face in rgb_faces:
#     print("face number: %s" %i)
#     plt.figure("face number %s" %i)
#     plt.imshow(face)
#     i+= 1
#
# score= cosine(get_embedding(expand_dims(rgb_faces[0], axis=0)), get_embedding(expand_dims(rgb_faces[1], axis=0)))
cosi= cosine(score, score1)
print("score= ", cosi)
# plt.figure("2")
# plt.imshow(rgb_face1)

# plt.show()

# print("0 0 index ", rgb_faces[0])
# print("complete lis: ", rgb_faces)


