#History:
#encountered many difficulties at generalizing extract_faces
#module,  altered it back to original way of doing
#now it return the only face in picture
#so may expect change of logic in this module


import os
import cv2


#Imports to work with deep face
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

import rec_by_deepface as df




picture= "extracted_face_picture/single_face_picture.jpg"
picture= Image.open(picture)
#picture = cv2.imread(picture)[:, :, ::-1]
picture= picture.resize((160,160))
#going to work with deepface
i=0

frames_from_npz= "video_faces.npz"
frames= np.load(frames_from_npz)
frames= frames["arr_0"]
frame_num=1
for frames_arr in frames:
    # frame= Image.fromarray(frames_arr)


#    plt.imshow(picture)
#    plt.show()
#    break
#     print(frames_arr)
#     print(np.array(frame))
    df.verify(np.array(picture),frames_arr, "Facenet")
    print(i, "Above reuslts are for frame", frame_num)
    frame_num+= 1
    i+= 1

#below plotting just for initial test purpose
#print(face_picture_input)
#pyplot.imshow(face_picture_input)
#pyplot.show()