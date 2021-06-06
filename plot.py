import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

fig=plt.figure(figsize=(8, 8))

def plot_from_npz():
    faces_np_name= "video_faces.npz"
    faces= np.load(faces_np_name)
    faces= faces["arr_0"]
    i=1
    print(len(faces))
    colrows= 12
    for face_arr in faces:
        #print(face)
        face= Image.fromarray(face_arr)
        fig.add_subplot(colrows, colrows, i)
        plt.imshow(face)
        i+= 1
    plt.show()

def testplot():
    picture = "extracted_face_picture/single_face_picture.jpg"
    picture = Image.open(picture)
    # picture = cv2.imread(picture)[:, :, ::-1]
    picture = picture.resize((160, 160))
    plt.imshow(picture)

def testplot1():
    frames_from_npz = "video_faces.npz"
    frames = np.load(frames_from_npz)
    frames = frames["arr_0"]
    frame_num = 1
    for frames_arr in frames:
        frame = Image.fromarray(frames_arr)
        plt.imshow(frame)
testplot1()