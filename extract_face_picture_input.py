#History:
#tested many thing in last couple of days
#its been hard to to generalise this module for face input
#and video input, now while testing detection in video file
#I altered many logics, I am going to change logic in this
#too putting an end to efforts at generalizing only module
#for pic and video input, later I may reverse this decison


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

    for face in results:
        x1, y1, width, height= results[0]['box']
        x2, y2, = x1+width, y1+height

        #extract face
        face= img_array[y1:y2, x1:x2]

        #resizing for the model
        image= Image.fromarray(face)
        image= image.resize(scale_size)

        #setting face path for picture input, saving it in directory
        face_folder= "extracted_face_picture/"
        face_name= "single_face_picture.jpg"
        path_of_picture_face=face_folder+ face_name
        #saving
        image.save(path_of_picture_face)

        face_array= asarray(image)
    return face_array



#to extract single face from picture
#some imports are done here we can avoid them in main.py
from PIL import Image
from numpy import asarray
from mtcnn.mtcnn import MTCNN

picture_folder= 'pic_input/'

# path for picture input
path = picture_folder + "single-face-pic-input.jpg"
# get face
face_picture_input = extract_faces(path)


