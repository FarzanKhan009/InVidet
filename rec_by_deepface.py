#It is testing module will implement deepface using different
#models including faceNet, main purpose is to align the progress
#and testing performance of different models

#imports
from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt

def verify(img, frame, model):
    results= DeepFace.verify(img, frame, enforce_detection=False, model_name=model)
    print("result: ", results)
    verification= results['verified']
    if verification is True:
        print(model, "Successfully recognised. SCORE=")
        return
    return
