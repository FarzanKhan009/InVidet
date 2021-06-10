import glob

import PySimpleGUI as sg
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from extract_face_nparray import extract_face
from create_npz_file import create_npz_faces
from plot import plot_from_npz
from face_compare import compare_faces

#getting face np array

def get_face(picture_input):
    # slicing path string because folder reside in project directory
    picture_input = picture_input.rsplit("InVidett", 1)
    picture_input = picture_input[1][1:]
    # calling module extract_face_nparraay to get the face list
    return extract_face(picture_input)

# def get_video_npz(video_input):
#     video_input= video_input.rsplit("InVidett",1)[1][1:]
#
#     # return create_npz_faces(video_input)
#
#     # creating npz file
#     create_npz_faces(video_input)
#     return np.load("video_faces.npz")["arr_0"]

# def get_video_faces_list(video_input):
#     video_input = video_input.rsplit("InVidett", 1)[1][1:]
#     return create_npz_faces(video_input)


sg.theme('BluePurple')
layout_column = [
        [sg.Text('InVid Detector',justification='center', font="Courier 20")],
        ]

# title_layout=[sg.Column([sg.T("InVid Detector", justification="center")], element_justification="center")]
# title_column=
input_layout= [[sg.T('Select Picture', pad=((20,10),30)), sg.In(key='-PICIN-', pad=((10,10),30)), sg.FilesBrowse(target='-PICIN-', pad=((10,50),30)), sg.T('Select Video', pad=((50,10),30)), sg.In(key='-VIDIN-', pad=((10,10),30)), sg.FilesBrowse(target='-VIDIN-', pad=((10,20),30))]]


layout =[
        [sg.Column(layout_column, element_justification='center', pad=(440,0))],
        input_layout,
        [sg.B("OK", key="-OK-")]
        ]



window = sg.Window('InVid Detector', layout, size=(1200, 800),)
while True:  # Event Loop
    event, values = window.read()
    # print(event, values["-PICIN-"])
    # print(values["pic_in"])
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-OK-':
        picture_input=values["-PICIN-"]
        pic_face= get_face(picture_input)[0]

        video_input= values["-VIDIN-"]
        compare_faces(pic_face, video_input)

        # video_faces_list= get_video_faces_list(video_input)
        # video_faces_list= get_video_npz(video_input)

        # plot_from_npz(video_faces_list)


        # print(picture_input)
        # Update the "output" text element to be the value of "input" element
        # window['-OUTPUT-'].update(values['-IN-'])

window.close()