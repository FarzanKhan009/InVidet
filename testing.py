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

def get_embedding(face):
    embeddings = FaceNet().embeddings(face)
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
        x2, y2, = x1 + width, y1 + height

        # extracting this face from frame_array
        frame_face = frame_array[y1:y2, x1:x2]


        print("face no: %s" % face_num)
        mtcn_face.append(frame_face)
        frame_face = DeepFace.detectFace(frame_face, detector_backend='mtcnn')
        # except:
        #     print("Face is not detected by deepface")
        rgb_face = frame_face[:, :, ::-1]
        rgb_face = cv2.resize(rgb_face, dsize=(160, 160), interpolation=cv2.INTER_CUBIC)
        # print(rgb_face.shape, type(rgb_face))
        # plt.figure("face_num+1")
        # plt.imshow(rgb_face)
        rgb_faces.append(rgb_face)
        face_num += 1



# print(frame_face)
# print(get_embedding(frame_face))
# print(rgb_face.shape, type(rgb_face))
# plt.figure("1")
# plt.imshow(rgb_face)

# rgb_face= fromarray(rgb_face).resize((160,160))
i=0
for face in rgb_faces:
    if i==2:
        print(face.shape, type(face))
        plt.figure("figure no %s" % i)
        plt.imshow(face)
        plt.imshow(mtcn_face[2])
    i+=1
# plt.figure("2")
# plt.imshow(rgb_face1)
plt.show()