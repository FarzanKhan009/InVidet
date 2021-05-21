from extract_faces import extract_faces
from os import listdir
from numpy import asarray
from PIL import Image
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
folder= 'pic_input/'

i=0
j=1
for filename in listdir(folder):
	# path
	path = folder + filename
	# get face
	faces_list = extract_faces(path)

	print(i, faces_list[0].shape)
	# plot
	pyplot.subplot(1, 2, j)
	pyplot.axis('off')
	pyplot.imshow(faces_list[0])
	i += 1
	j += 1
	if i==2:
		break
pyplot.show()