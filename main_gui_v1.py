import glob
from sys import exit

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





#                                                      ──────▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
#                                                      ───▄▄██▌█ Setting Layouts
#                                                        ▄▄▄▌▐██▌█
#                                                       ███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄​▄▌
#                                                        ▀(@)▀▀▀▀▀▀▀(@)(@)▀▀▀▀▀▀▀▀▀▀▀▀(​@)▀▘ ::

# to use in padding tupple
inputs_pad_standard= ((5,5),10)
setting_pad= ((20,10), (1,1))
h1= "Akira 30"
h2= "Akira 25"
h3= "Akira 10"
h33= "Akira 15"
# theme
sg.theme('BluePurple')

# title layout
title_layout = [[
    sg.Text('InVid Detector',justification='center', font=h1)
]]

# taking inputs/ url for picture and video file, layout
picture_video_selection_layout= [
    [sg.T("Inputs", font=h2, pad=inputs_pad_standard)],
    [sg.T('Select Picture', pad=inputs_pad_standard, key="-SPIC-", size=(20,1), font=h33), sg.In(key='-PICIN-', pad=inputs_pad_standard, visible=False),
    sg.FilesBrowse(target='-PICIN-', pad=inputs_pad_standard)],

    [sg.T('Select Video', pad=inputs_pad_standard, key="-SVID-", size=(20,1), font=h33), sg.In(key='-VIDIN-', pad=inputs_pad_standard, visible=False),
    sg.FilesBrowse(target='-VIDIN-', pad=inputs_pad_standard)]
]

# person name input
person_name_layout= [
    [sg.T("Setting", font=h2, pad=setting_pad)],
    [sg.Text("Person name if known? (optional)", pad=setting_pad, font=h33)],
    [sg.Input(key="-PNAME-", size=(16,1), pad=setting_pad, font=h3)]
]


# threshold layout setting
threshold_layout=[
    [sg.T("Select a threshold value", pad=setting_pad, font=h33)],
    [sg.Radio('0.4', "RADIO1", size=(4, 1), pad= setting_pad, font=h3, key="-TH1-"),
    sg.Radio('0.5', "RADIO1", default=True, size=(4, 1), pad= setting_pad, font=h3, key="-TH2-"),
    sg.Radio('0.6', "RADIO1", size=(4,1), pad= setting_pad, font=h3, key="-TH3-")]
]

# verifying fps layout
verifying_layout=[
    [sg.T("Select Verifying fps", pad=setting_pad, font=h33)],
    [sg.Radio("V1FPS", "RADIO2", default=True, font=h3, pad=setting_pad, size=(6,1), key="-FPS1-"), sg.Radio("V2FPS", "RADIO2", font=h3, pad=setting_pad, size=(6,1), key="-FPS2-")],
    [sg.Radio("V3FPS", "RADIO2", font=h3, pad=setting_pad, size=(6,1), key="-FPS3-"), sg.Radio("V4FPS", "RADIO2", font=h3, pad=setting_pad, size=(6,1), key="-FPS4-")]
]

# video write or not
write_video_layout=[
[sg.T("Want to write/output a video file?", pad=setting_pad, font=h33)],
    [sg.Radio("No", "RADIO3", default=True, font=h3, pad=setting_pad, size=(6,1), key="-VOUT1-"), sg.Radio("Yes", "RADIO3", font=h3, pad=setting_pad, size=(6,1), key="-VOUT2-")]
]


# final layout/ integrated layout
layout =[
    [sg.Column(title_layout, element_justification='center', pad=(440,0))],
    picture_video_selection_layout,
    [sg.B("Load Inputs", key="-LOAD-", pad=inputs_pad_standard)],
    person_name_layout,
    threshold_layout,
    verifying_layout,
    write_video_layout,
    [sg.B("SET", key='-SET-', pad=setting_pad)]
]

# starting windows
window = sg.Window('InVid Detector', layout, size=(1200, 800), finalize=True)




#                                                      ──────▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
#                                                      ───▄▄██▌█ Handling Events
#                                                        ▄▄▄▌▐██▌█
#                                                       ███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄​▄▌
#                                                        ▀(@)▀▀▀▀▀▀▀(@)(@)▀▀▀▀▀▀▀▀▀▀▀▀(​@)▀▘ ::





while True:  # Event Loop
    event, values = window.read()
    # print(event, values["-PICIN-"])
    # print(values["pic_in"])
    if event == sg.WIN_CLOSED or event == 'Exit':
        exit()
        break
    if event == "-SET-":
        # setting threshold
        if window["-TH1-"].get():
            threshold= 0.4
        if window["-TH2-"].get():
            threshold= 0.5
        if window["-TH3-"].get():
            threshold= 0.6

        # setting fps
        if window["-FPS1-"].get():
            fps= 1
        if window["-FPS2-"].get():
            fps= 2
        if window["-FPS3-"].get():
            fps= 3
        if window["-FPS4-"].get():
            fps= 4

        # setting video write choice
        if window["-VOUT1-"].get():
            v_out= False
        if window["-VOUT2-"].get():
            v_out= True

        print("thresholds: ", threshold)
        print("FPS: ", fps)
        print("V_OUT", v_out)
    if event == '-LOAD-':
        picture_input=values["-PICIN-"]
        window["-SPIC-"].update("Picture is SELECTED")
        video_input= values["-VIDIN-"]
        window["-SVID-"].update("Video is SELECTED")



        # threshold= window["TH1"].get()
        # print(threshold, type(threshold))


        track_records= [] #compare_faces(picture_input, video_input)
        if len(track_records) >0:
            for frames in track_records:
                current_index= track_records.index(frames)
                if current_index % 2 ==0:
                    last_frame= track_records[current_index+1]
                    print("\n\nResults")
                    print("Matched was found:")
                    print("From frame number ", frames, " to ", last_frame)
                    print("That is approximately Face Matched during time ", frames/32, "sec to ", last_frame/32)

            if len(track_records) % 2 != 0:
                first_frame = track_records[len(track_records) - 2]
                last_frame = track_records[len(track_records) - 1]
                print("\n\nResults")
                print("Matched was found:")
                print("From frame number ", frames, " to ", last_frame)
                print("That is approximately Face Matched during time ", first_frame / 32, "sec to ", last_frame / 32)
        # video_faces_list= get_video_faces_list(video_input)
        # video_faces_list= get_video_npz(video_input)

        # plot_from_npz(video_faces_list)


        # print(picture_input)
        # Update the "output" text element to be the value of "input" element
        # window['-OUTPUT-'].update(values['-IN-'])

window.close()