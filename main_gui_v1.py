import glob
from sys import exit
from moviepy.editor import VideoFileClip
import PySimpleGUI as sg
import numpy as np
from PIL import Image
from cv2 import cv2
from matplotlib import pyplot as plt

from extract_face_nparray import extract_face
from create_npz_file import create_npz_faces
from plot import plot_from_npz
from face_compare import compare_faces





#                                                      ──────▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
#                                                      ───▄▄██▌█ Global Variable Initialization
#                                                        ▄▄▄▌▐██▌█
#                                                       ███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄​▄▌
#                                                        ▀(@)▀▀▀▀▀▀▀(@)(@)▀▀▀▀▀▀▀▀▀▀▀▀(​@)▀▘ ::

threshold, v_fps, fps, duration =0.5,1,0,0
v_out= False
picture_input, video_input ="", ""
aprx_ratio= 0.75
time = (duration * aprx_ratio) + 10















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
setting_pad= ((5,5), (1,1))
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
    [sg.Input(key="-PRNAME-", size=(16,1), pad=setting_pad, font=h3)]
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

# video detail layout
input_details_layout=[
    [sg.T("Details on input", pad=setting_pad, font=h33, size=(24,1))],
    [sg.T("Picture name: ", pad=setting_pad, font=h3, key="-PNAME-", size=(24,1))],
    [sg.T("Video name: ", pad=setting_pad, font=h3, key="-VNAME", size=(24,1))],
    [sg.T("Video frame rate: ", pad=setting_pad, font=h3, key="-VFPS-", size=(24,1))],
    [sg.T("Video duration: ", pad=setting_pad, font=h3, key="-VDUR-", size=(24,1))]
]

# setting choices layout
set_choice_layout=[
    [sg.T("Set Threshold\t: 0.5   (default)", pad=setting_pad, font=h3, key="-DFLT1-", size=(30,1))],
    [sg.T("V_Frame Rate\t: 1FPS  (default)", pad=setting_pad, font=h3, key="-DFLT2-", size=(30, 1))],
    [sg.T("Write Video\t: NO    (default)", pad=setting_pad, font=h3, key="-DFLT3-", size=(30, 1))],
    [sg.T("Estimated time to process: ", pad=setting_pad, font=h3, key="-APRX-", size=(24, 1))]
]

# BAR_MAX = 1000
# progress_bar_layout = [
#     [sg.Text('A custom progress meter')],
#     [sg.ProgressBar(BAR_MAX, orientation='h', size=(20,20), key='-PROG-')],
#     [sg.Cancel()]
# ]

# approximate time to process



# final layout/ integrated layout
layout =[
    [sg.Column(title_layout, element_justification='center', pad=(440,0))],
    picture_video_selection_layout,
    input_details_layout,
    [sg.B("Load Inputs", key="-LOAD-", pad=inputs_pad_standard)],
    person_name_layout,
    threshold_layout,
    verifying_layout,
    write_video_layout,
    set_choice_layout,
    [sg.B("SET", key='-SET-', pad=setting_pad), sg.B("Start Processing", key='-START-', pad=setting_pad)],
    # progress_bar_layout
]

# starting windows
window = sg.Window('InVid Detector', layout, size=(1200, 900), finalize=True)




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
            window["-DFLT1-"].update("Set Threshold\t: 0.4")
            threshold= 0.4
        if window["-TH2-"].get():
            window["-DFLT1-"].update("Set Threshold\t: 0.5   (default)")
            threshold= 0.5
        if window["-TH3-"].get():
            window["-DFLT1-"].update("Set Threshold\t: 0.6")
            threshold= 0.6

        # setting fps
        if window["-FPS1-"].get():
            window["-DFLT2-"].update("V_Frame Rate\t: 1FPS  (default)")
            aprx_ratio= 0.75
            time = (duration * aprx_ratio) + 10
            window["-APRX-"].update("Estimated time to process: %s" % time)
            v_fps= 1
        if window["-FPS2-"].get():
            window["-DFLT2-"].update("V_Frame Rate\t: 2FPS")
            aprx_ratio= 1.5
            time = (duration * aprx_ratio) + 10
            window["-APRX-"].update("Estimated time to process: %s" % time)
            v_fps= 2
        if window["-FPS3-"].get():
            window["-DFLT2-"].update("V_Frame Rate\t: 3FPS")
            aprx_ratio= 2.25
            time = (duration * aprx_ratio) + 10
            window["-APRX-"].update("Estimated time to process: %s" % time)
            v_fps= 3
        if window["-FPS4-"].get():
            window["-DFLT2-"].update("V_Frame Rate\t: 4FPS")
            aprx_ratio= 3
            time= (duration* aprx_ratio)+10
            window["-APRX-"].update("Estimated time to process: %s" %time)
            v_fps= 4

        # setting video write choice
        if window["-VOUT1-"].get():
            window["-DFLT3-"].update("Write Video\t: NO    (default)")
            v_out= False
        if window["-VOUT2-"].get():
            window["-DFLT3-"].update("Write Video\t: YES")
            v_out= True

        print("thresholds: ", threshold)
        print("FPS: ", v_fps)
        print("V_OUT", v_out)
        print("Estimated time to process: ", (duration* aprx_ratio)+10)    # 0.75 is ratio on my pc for v1FPS


    if event == '-LOAD-':
        picture_input=values["-PICIN-"]
        video_input= values["-VIDIN-"]
        window.refresh()
        if len(picture_input)>0:
            window["-SPIC-"].update("Picture is SELECTED")
            pic_url = picture_input.rsplit("/", 1)
            pic_url = "Picture name: %s" % pic_url[1]
            window["-PNAME-"].update(value=str(pic_url))

        if len(video_input)>0:
            window["-SVID-"].update("Video is SELECTED")
            # obtaining fps and setting text

            vid_url = video_input.rsplit("dett", 1)
            vid_url = vid_url[1][1:]
            # print(vid_url)
            cam = cv2.VideoCapture(vid_url)
            fps = cam.get(cv2.CAP_PROP_FPS)
            clip= VideoFileClip(vid_url)
            duration= clip.duration
            vid_name = vid_url.rsplit("/", 1)
            # print(vid_name, pic_url)
            vid_name = f'{"Video name: "}{vid_name[1]}'
            message_fps = "Video frame rate: %s" % fps
            # print(vid_name, fps, pic_url)
            # window.refresh()
            window["-VNAME"].update(value=str(vid_name))
            window["-VFPS-"].update(value=str(message_fps))
            window["-VDUR-"].update(value= f'{"Video duration: "}{duration}{"sec"}')

        # window.refresh()



        # threshold= window["TH1"].get()
        # print(threshold, type(threshold))
    if event == "-START-":
        if len(picture_input)>0 and len(video_input)>0:
            track_records= compare_faces(picture_input, video_input, fps, threshold, v_out, v_fps)
            # track_records= compare_faces(picture_input, video_input)
            if len(track_records) >0:
                for frames in track_records:
                    current_index= track_records.index(frames)
                    if current_index % 2 ==0:
                        last_frame= track_records[current_index+1]
                        print("\n\nResults")
                        print("Matched was found:")
                        print("From frame number ", frames, " to ", last_frame)
                        print("That is approximately Face Matched during time ", frames/(fps+2), "sec to ", last_frame/(fps+2))

                if len(track_records) % 2 != 0:
                    first_frame = track_records[len(track_records) - 2]
                    last_frame = track_records[len(track_records) - 1]
                    print("\n\nResults")
                    print("Matched was found:")
                    print("From frame number ", frames, " to ", last_frame)
                    print("That is approximately Face Matched during time ", first_frame / (fps+ 2), "sec to ", last_frame / (fps+2))       # +2 in fps is for bugg fixes
        else:
            print("Inputs are not set yet!")

window.close()