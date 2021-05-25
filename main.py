#History:
#encountered many difficulties at generalizing extract_faces
#module,  altered it back to original way of doing
#now it return the only face in picture
#so may expect change of logic in this module
import os

from extract_faces import extract_faces
from os import listdir
from numpy import asarray
from PIL import Image
import cv2
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN

#Imports to work with deep face
import rec_by_deepface as df






#going to work with deepface
i=0
for files in os.listdir("video_frames/"):
    frames = cv2.imread("video_frames/%s" %(files))[:, :, ::-1]

    try:
        df.verify(path, frames)
        i+= 1
        print("no", i, "frame name: ", files)
    except:
        print("Face might not been detected for file %s" %(i))
        i+= 1

#below plotting just for initial test purpose
#print(face_picture_input)
#pyplot.imshow(face_picture_input)
#pyplot.show()