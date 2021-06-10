import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def plot_from_npz(loaded_npz):
    fig = plt.figure(figsize=(8, 8))

    # faces= np.load(str(url))
    # faces= faces["arr_0"]
    # faces= np.load("video_faces.npz")["arr_0"]
    faces= loaded_npz
    i=1
    # print(loaded_npz)
    # print(np.load("video_faces.npz")["arr_0"])
    # print(len(faces))
    colrows= 12
    for face_arr in faces:
        #print(face)
        face= Image.fromarray(face_arr)
        # fig.add_subplot(colrows, colrows, i)
        plt.imshow(face)
        i+= 1
    plt.show()
    return

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
# testplot1()
# plot_from_npz("kkk")