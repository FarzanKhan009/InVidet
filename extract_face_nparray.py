from PIL import Image
from mtcnn_cv2 import MTCNN
from numpy import asarray


def extract_face(url):
    image= Image.open(url)
    image= image.convert('RGB')
    img_array= asarray(image)


    detector= MTCNN()

    results= detector.detect_faces(img_array)
    face_num=0
    faces_list= list()
    for faces in results:
        x1, y1, width, height = results[face_num]['box']
        x2, y2, = x1 + width, y1 + height

        # extract face
        face= img_array[y1:y2, x1:x2]

        # resizing for the model
        face = Image.fromarray(face)
        face = face.resize((160,160))

        #converting it back to arrray to append the list
        face= asarray(face)
        faces_list.append(face)
        face_num+= 1

    return faces_list

