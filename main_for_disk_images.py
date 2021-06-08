#History:
#encountered many difficulties at generalizing extract_faces
#module,  altered it back to original way of doing
#now it return the only face in picture
#so may expect change of logic in this module


import os
import cv2


#Imports to work with deep face
import matplotlib.pyplot as plt

import rec_by_deepface as df




picture= "extracted_face_picture/single_face_picture.jpg"
picture = cv2.imread(picture)[:, :, ::-1]
#going to work with deepface
i=0
for files in os.listdir("extracted_faces_video_frames"):
    frames = cv2.imread("extracted_faces_video_frames/%s" %(files))[:, :, ::-1]

#    plt.imshow(picture)
#    plt.show()
#    break

    try:
        #vf= df.verify(picture, frames, "VGG-Face", vf, fn, of, dff, did, af,dlb)
        df.verify(picture,frames, "Facenet")
        # #of= df.verify(picture, frames, "OpenFace", vf, fn, of, dff, did, af,dlb)
        # dff= df.verify(picture, frames, "DeepFace", vf, fn, of, dff, did, af,dlb)
        # did= df.verify(picture, frames, "DeepID", vf, fn, of, dff, did, af,dlb)
        # af= df.verify(picture, frames, "ArcFace", vf, fn, of, dff, did, af,dlb)
        # dlb= df.verify(picture, frames, "Dlib", vf, fn, of, dff, did, af,dlb)
        i+= 1
        print(i, "Above reuslts are for frame", files)
    except:
        print("Face might not been detected for file %s" %(i))
        i+= 1

#below plotting just for initial test purpose
#print(face_picture_input)
#pyplot.imshow(face_picture_input)
#pyplot.show()