#History:
#encountered many difficulties at generalizing extract_faces
#module,  altered it back to original way of doing
#now it return the only face in picture
#so may expect change of logic in this module


from extract_faces import extract_faces
from os import listdir
from numpy import asarray
from PIL import Image
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
picture_folder= 'pic_input/'

# path
path = picture_folder + "single-face-pic-input.jpg"
# get face

face_picture_input = extract_faces(path)
#below plotting just for initial test purpose
#print(face_picture_input)
#pyplot.imshow(face_picture_input)
#pyplot.show()