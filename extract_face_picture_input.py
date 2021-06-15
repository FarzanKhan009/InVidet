#History:
#tested many thing in last couple of days
#its been hard to to generalise this module for face input
#and video input, now while testing detection in video file
#I altered many logics, I am going to change logic in this
#too putting an end to efforts at generalizing only module
#for pic and video input, later I may reverse this decison
import math

import matplotlib.pyplot as plt
import numpy as np
import cv2




def align_face(image, location, leftEyePts, rightEyePts):

    # load image and find face locations.

    # image = face_recognition.load_image_file("sample.jpg")
    # face_locations = face_recognition.face_locations(image, model="hog")

    # detect 68-landmarks from image. This includes left eye, right eye, lips, eye brows, nose and chins
    # face_landmarks = face_recognition.face_landmarks(image)

    '''
    Let's find and angle of the face. First calculate 
    the center of left and right eye by using eye landmarks.
    '''
    # leftEyePts = face_landmarks[0]['left_eye']
    # rightEyePts = face_landmarks[0]['right_eye']

    leftEyeCenter = np.array(leftEyePts).mean(axis=0).astype("int")
    rightEyeCenter = np.array(rightEyePts).mean(axis=0).astype("int")

    leftEyeCenter = (leftEyeCenter[0], leftEyeCenter[1])
    rightEyeCenter = (rightEyeCenter[0], rightEyeCenter[1])

    # draw the circle at centers and line connecting to them
    cv2.circle(image, leftEyeCenter, 2, (255, 0, 0), 10)
    cv2.circle(image, rightEyeCenter, 2, (255, 0, 0), 10)
    cv2.line(image, leftEyeCenter, rightEyeCenter, (255, 0, 0), 10)

    # find and angle of line by using slop of the line.
    dY = rightEyeCenter[1] - leftEyeCenter[1]
    dX = rightEyeCenter[0] - leftEyeCenter[0]
    angle = np.degrees(np.arctan2(dY, dX))

    # to get the face at the center of the image,
    # set desired left eye location. Right eye location
    # will be found out by using left eye location.
    # this location is in percentage.
    desiredLeftEye = (0.35, 0.35)
    # Set the croped image(face) size after rotaion.
    desiredFaceWidth = 128
    desiredFaceHeight = 128

    desiredRightEyeX = 1.0 - desiredLeftEye[0]

    # determine the scale of the new resulting image by taking
    # the ratio of the distance between eyes in the *current*
    # image to the ratio of distance between eyes in the
    # *desired* image
    dist = np.sqrt((dX ** 2) + (dY ** 2))
    desiredDist = (desiredRightEyeX - desiredLeftEye[0])
    desiredDist *= desiredFaceWidth
    scale = desiredDist / dist

    # compute center (x, y)-coordinates (i.e., the median point)
    # between the two eyes in the input image
    eyesCenter = ((leftEyeCenter[0] + rightEyeCenter[0]) // 2,
                  (leftEyeCenter[1] + rightEyeCenter[1]) // 2)

    # grab the rotation matrix for rotating and scaling the face
    M = cv2.getRotationMatrix2D(eyesCenter, angle, scale)

    # update the translation component of the matrix
    tX = desiredFaceWidth * 0.5
    tY = desiredFaceHeight * desiredLeftEye[1]
    M[0, 2] += (tX - eyesCenter[0])
    M[1, 2] += (tY - eyesCenter[1])

    # apply the affine transformation
    (w, h) = (desiredFaceWidth, desiredFaceHeight)
    (y2, x2, y1, x1) = location

    output = cv2.warpAffine(image, M, (w, h),
                            flags=cv2.INTER_CUBIC)

    # cv2.imshow('image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return output



def extract_faces(path, scale_size=(160,160)):
    #scale_size is kind of required to get the best output
    #load the image/ frame
    image= Image.open(path)

    #convert to RGB for better efficiency at detecting to standardize the color scheme
    image= image.convert('RGB')

    #convert to array
    img_array= asarray(image)

    #loading detector
    detector= MTCNN()

    #detecting and storing to results object
    results= detector.detect_faces(img_array)
    # print(results)

    for face in results:
        # [{'box': [1413, 1458, 1022, 1387], 'confidence': 0.9999998807907104, 'keypoints': {'left_eye': (1731, 2008), 'right_eye': (2196, 2037), 'nose': (2001, 2362), 'mouth_left': (1754, 2542), 'mouth_right': (2143, 2558)}}]
        print("left_eye", results[0]["keypoints"]["left_eye"])
        print("right_eye", results[0]["keypoints"]["right_eye"])

        left_eye= results[0]["keypoints"]["left_eye"]
        right_eye= results[0]["keypoints"]["left_eye"]


        x1, y1, width, height= results[0]['box']
        x2, y2, = x1+width, y1+height

        #extract face
        face= img_array[y1:y2, x1:x2]
        # aligned_image= alignment_procedure(face, results[0]["keypoints"]["left_eye"], results[0]["keypoints"]["right_eye"])
        # mt = functions.align_face(img=face, detector_backend=backends[3])
        # dl = functions.align_face(img=face, detector_backend=backends[2])




        #resizing for the model
        image= Image.fromarray(face)
        aligned_face = align_face(image, results[0]['box'], left_eye, right_eye)
        image= image.resize(scale_size)

        #setting face path for picture input, saving it in directory
        face_folder= "extracted_face_picture/"
        face_name= "single_face_picture.jpg"
        path_of_picture_face=face_folder+ face_name
        #saving
        image.save(path_of_picture_face)

        face_array= asarray(image)
    return [face_array, aligned_face]



#to extract single face from picture
#some imports are done here we can avoid them in main.py
from PIL import Image
from numpy import asarray
from mtcnn_cv2 import MTCNN

picture_folder= 'pic_input/'

# path for picture input
path = picture_folder + "single-face-pic-input.jpg"
extract= extract_faces(path)

face= extract[0]
align_face= extract[1]

plt.figure("extracted face")
plt.imshow(face)

plt.figure("aligned")
plt.imshow(align_face)

plt.show()



# pic_in= extract_faces()

# plt.figure("simple face")
# plt.imshow(plt.imread(path))

# get face
# list_of= extract_faces(path)
# face_picture_input, aligned_image, dl = list_of[0], list_of[1], list_of[2]
# plt.figure("extracted")
# plt.imshow(face_picture_input)
# plt.figure("aligned")
# plt.imshow(aligned_image)
# //
# plt.figure("mtcnn")
# plt.imshow(mt)
# plt.figure("dlib")
# plt.imshow(dl)
# plt.show()



