#to extract faces from picture or frame of a video
#some imports are done here we can avoid them in main.py

#cut and pasted imports altering logic****

#to generalize each pic or frame we try returning the list containing multiple faces
#arrays for each face in a pic, on the input side of picture i would recommend
#take the single face out from this list

def extract_faces(path, scale_size=(160,160)): #scale_size is kind of required to get the best output
    #load the image/ frame
    image= Image.open(path)

    #convert to RGB for better efficiency at detecting to standardize the color scheme
    image= image.convert('RGB')

    #convert to array
    img_array= asarray(iamge)

    #creating detector
    detector= MTCNN()

    #detecting and storing to results object
    results= detector.detect_faces(img_array)

    #trying to handle multiple faces
    i=0
    faces= list()
    for face in results:
        x1, y1, width, height= results[i]['box']
        x2, y2, = x1+width, y1+height

        #extract face
        face= img_array[y1:y2, x1:x2]

        #resizing for the model
        image= Image.fromarray(face)
        image= image.resize(scale_size)
        face_array= asarray(image)
        faces.append(face_array)
    return faces
