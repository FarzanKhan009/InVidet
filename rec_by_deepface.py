#It is testing module will implement deepface using different
#models including faceNet, main purpose is to align the progress
#and testing performance of different models

#imports
from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt

def verify(img, frame):
    results= DeepFace.verify(img, frame, model_name="Facenet")
    print("result: ", results)
    verification= results[0]
    if verification:
        print("they are same")
    else:
        print("not same")
