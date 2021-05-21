from extract_faces import extract_faces
from os import listdir
import numpy
import Image
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN

folder= 'pic_input'
i=0
for filename in listdir(folder):
	# path
	path = folder + filename
	# get face
	faces_list = extract_faces(path)

	print(i, faces_list[i].shape)
	# plot
	pyplot.subplot(1, 3, i)
	pyplot.axis('off')
	pyplot.imshow(face)
	i += 1
pyplot.show()