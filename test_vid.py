import cv2
from mtcnn_cv2 import MTCNN
from numpy import asarray

from PIL import Image


#History:
#first implemented dlib face_recognition module detect faces
#But dlibs' accuracy was very poor at detecting faces in video file
#So followed the same i.e. mtcnn which used in detecting faces in picture
#now removing all dlibs imports and scrap code in comments
#version 2:
#changing some lines + adding some lines to extract video frames
#to work with deepface



#opening video file using cv2
cap= cv2.VideoCapture("vid_input/multi-face.mp4")

#loop to monitor enter key to terminate and iterate video frames
countframes=0
while True:
    # Grab a single frame of video
    ret, frame = cap.read()
    countframes += 1

    #below if conditional logic is to boost up the speed
    #reducing frames rate 6 fps actual was 30fps
    if countframes %5 != 0:
        continue


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
        #to work with deep face
        frame_array = asarray(frame)

        #taking variable face_num; to iterate in loop; for detecting multiple faces in single frame
        face_num=0
        for face in result:
            #if confused read the documentation of cv2.rectangle() it would help a lot

            #starting point of the face is stored in x1, y1 as tupple i.e. (x1,y1)
            x1, y1, width, height= result[face_num]['box']
            #storing ending points in x2, y2
            x2, y2, = x1+width, y1+height

            #rather than drawing rectangle I would want to save faces
            #appeared in frames to a directory; to work with deepface

            #creating image from image array to store in directory video_frames
            frame_face = frame_array[y1:y2, x1:x2]
            frame_face = Image.fromarray(frame_face).convert('RGB') #conveerted RGB

            #setting a trackable name
            face_name= f'{countframes}{"-"}{face_num}'
            frame_path= "video_frames/"+ face_name+ ".jpg"
            #saving single face of frame in directory
            frame_face.save(frame_path)

            #cv2.rectangle(start, end, color(RGB), (pixel of drawn line))
            #drawing rectangle araound the face
            cv2.rectangle(frame, (x1,y1),
                            (x2,y2), (0, 155, 255),2)
            face_num+= 1

    # Display the resulting frames video
    cv2.imshow('Video', frame)
    print(countframes)

    # Wait for Enter key to stop
    if cv2.waitKey(25) == 13 or frame is None :
        break


#releasing video and destroying windows
cap.release()
cv2.destroyAllWindows()
