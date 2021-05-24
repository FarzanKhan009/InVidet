import cv2
from mtcnn_cv2 import MTCNN


#History:
#first implemented dlib face_recognition module detect faces
#But dlibs' accuracy was very poor at detecting faces in video file
#So followed the same i.e. mtcnn which used in detecting faces in picture
#now removing all dlibs imports and scrap code in comments

#opening video file using cv2
cap= cv2.VideoCapture("vid_input/multi-face.webm")

#loop to monitor enter key to terminate and iterate video frames
while True:
    # Grab a single frame of video
    ret, frame = cap.read()
    # Convert the image from BGR color (which OpenCV uses) to RGB
    # RGB is preferred color while detection faces
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #another way of converting to RGB=>> rgb_frame = frame[:, :, ::-1]

    #loading detector from MTCNN
    detector = MTCNN()

    #saving all faces in result variable
    result = detector.detect_faces(rgb_frame)

    #if only one face in the frames
    print(result)

    if len(result) > 0:
        #taking variable i; to iterate in loop; for detecting multiple faces in single frame
        i=0
        for face in result:
            #if confused read the documentation of cv2.rectangle() it would help a lot

            #starting point of the face is stored in x1, y1 as tupple i.e. (x1,y1)
            x1, y1, width, height= result[i]['box']

            #storing ending points in x2, y2
            x2, y2, = x1+width, y1+height

            #cv2.rectangle(start, end, color(RGB), (pixel of drawn line))
            #drawing rectangle araound the face
            cv2.rectangle(frame, (x1,y1),
                            (x2,y2), (0, 155, 255),2)
            i+= 1

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Wait for Enter key to stop
    if cv2.waitKey(25) == 13:
        break


#releasing video and destroying windows
cap.release()
cv2.destroyAllWindows()
