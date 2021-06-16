import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from keras_facenet import FaceNet
from numpy import expand_dims
from scipy.spatial.distance import cosine

path= "pic_input/multiface.jpeg"
img= np.asarray(Image.open(path))

embedder= FaceNet()

faces = embedder.extract(path)

print(faces)
i=0
cr_face, pr_face= list(), list()
cr_face.append("")
pr_face.append("")
cr_face[0]= ""
pr_face[0]= ""
for face in faces:
    print(face['box'])
    x1, y1, width, height = face['box']
    # storing ending points in x2, y2
    print("extracted coordinates")
    x2, y2, = x1 + width,  y1 + height

    facen= img[y1:y2, x1:x2]
    print("cropped imaage")
    facen = expand_dims(facen, axis=0)
    embedding= embedder.embeddings(facen)
    if i>=1:
        pr_face= cr_face
        cr_face= embedding
    else:
        cr_face=embedding
    # plt.figure("Face No: %s" % i)
    # plt.imshow(facen)



    print(facen.shape)
    print("embeddings: ", embedding)
    i+=1

distance= cosine(cr_face[0], pr_face[0])
distance2= cosine(cr_face[0], cr_face[0])
print("both distances ", distance, distance2)
print(cr_face)

plt.show()