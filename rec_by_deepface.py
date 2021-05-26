#It is testing module will implement deepface using different
#models including faceNet, main purpose is to align the progress
#and testing performance of different models

#imports
from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt

def verify(img, frame, model, vf, fn, of, dff, did, af,dlb):
    results= DeepFace.verify(img, frame, enforce_detection=False, model_name=model)
    print("result: ", results)
    verification= results['verified']
    if verification is True:
        if model=="VGG-Face":
            print(model, "Successfully recognised. SCORE=", vf)
            vf+= 1
            return vf
        elif model=="Facenet":
            print(model, "Successfully recognised. SCORE=", fn)
            fn+= 1
            return fn
        elif model== "OpenFace":
            print(model, "Successfully recognised. SCORE=", of)
            of+= 1
            return of
        elif model== "DeepFace":
            print(model, "Successfully recognised. SCORE=", dff)
            dff+= 1
            return  dff
        elif model== "DeepID":
            print(model, "Successfully recognised. SCORE=", did)
            did+= 1
            return did
        elif model++ "ArcFace":
            print(model, "Successfully recognised. SCORE=", af)
            af+= 1
            return af
        elif model =="Dlib":
            print(model, "Successfully recognised. SCORE=", dlb)
            dlb+= 1
            return dlb
    else:
        if model== "VGG-Face":
            print(model, "!Successfully recognised. SCORE=", vf)
            #vf+= 1
        elif model== "Facenet":
            print(model, "!Successfully recognised. SCORE=", fn)
            #fn+= 1
        elif model== "OpenFace":
            print(model, "!Successfully recognised. SCORE=", of)
            #of+= 1
        elif model== "!DeepFace":
            print(model, "Successfully recognised. SCORE=", dff)
            #dff+= 1
        elif model== "DeepID":
            print(model, "!Successfully recognised. SCORE=", did)
            #did+= 1
        elif model++ "ArcFace":
            print(model, "!Successfully recognised. SCORE=", af)
            #af+= 1
        elif model =="Dlib":
            print(model, "!Successfully recognised. SCORE=", dlb)
            #dlb+= 1
        return
