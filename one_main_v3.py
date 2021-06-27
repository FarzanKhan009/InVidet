#                                                      ──────▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
#                                                      ───▄▄██▌█ Imports
#                                                        ▄▄▄▌▐██▌█
#                                                       ███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄​▄▌
#                                                        ▀(@)▀▀▀▀▀▀▀(@)(@)▀▀▀▀▀▀▀▀▀▀▀▀(​@)▀▘ ::
#```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
# it is to open text file in windows
import os
# it is to open text file in linux
import subprocess
# a simple GUI framework
import PySimpleGUI as sg
# to terminate the program on pressing exit button or window closing
from sys import exit
# to do operations on arrays of images
import numpy as np
# to read the live time
import times
# Image library help in reading images also creating images from arrays
from PIL import Image
# computer vision library to perform operations on images and videos
from cv2 import cv2
# keras implementation of facenet
from keras_facenet import FaceNet
# to expand dimensions
from keras.backend import expand_dims
# to calculate distances bw embeddings
from scipy.spatial.distance import cosine
# to read the monitors an obtain screen sizes
from screeninfo import get_monitors




#                                                      ──────▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
#                                                      ───▄▄██▌█ Some variables
#                                                        ▄▄▄▌▐██▌█
#                                                       ███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄​▄▌
#                                                        ▀(@)▀▀▀▀▀▀▀(@)(@)▀▀▀▀▀▀▀▀▀▀▀▀(​@)▀▘ ::
#```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
# getting screen size
width= get_monitors()[0].width
height= get_monitors()[0].height
screensize=(int(width), int(height))
print("[INFO] Reading screen size\n[INFO] size set to: ", screensize, "Type of: ", type(screensize))

# to carry addresses of picture and video file
vid_url,  pic_url= "",""
# it is to carry total frames from first read by cv2
total_frames = 0
# initializing these so any sub function can access that
picture_input, video_input, person_name ="", "", "Anonymous"
# setting defaults
threshold, v_fps, fps, frame_count, duration =0.5,1,1,0,0
v_out, v_show, video_file= False, False, True
# when estimating the time to take by process this ration can be
# multiplied with video duration when 1 vfps otherwise it change
aprx_ratio= 0.75
time = (duration * aprx_ratio) + 10
#to check first loop in GUI, for fetching results message in middle column
first = 0
# video source conditional check default 0 indicate video file
video_source_changing=0
# default divisible and tolerance
divisible = 0
tolerance = 5

# Loading model
encodder = FaceNet()


#                                                      ──────▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
#                                                      ───▄▄██▌█ GUI variable
#                                                        ▄▄▄▌▐██▌█  carrying fonts, size etc
#                                                       ███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄​▄▌
#                                                        ▀(@)▀▀▀▀▀▀▀(@)(@)▀▀▀▀▀▀▀▀▀▀▀▀(​@)▀▘ ::
#```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````


# to use in padding tupple
general_size= (int(width/90), 1)
output_height=int(height/18)
output_width=int(width/3)
result_height=int(height/25)

inputs_pad_standard= ((5,5),2)
setting_pad= ((5,5), (1,1))
login_pad= (5,10)
login_had1= "Akira 30"
login_had2= "Akira 25"
login_had3= "Akira 20"
login_had4= "Akira 14"
h1= "Akira 30"
h2= "Akira 25"
h3= "Akira 10"
h33= "Akira 15"
# theme
sg.theme('dark grey 5')




#                                                      ──────▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
#                                                      ───▄▄██▌█  Some functions
#                                                        ▄▄▄▌▐██▌█
#                                                       ███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄​▄▌
#                                                        ▀(@)▀▀▀▀▀▀▀(@)(@)▀▀▀▀▀▀▀▀▀▀▀▀(​@)▀▘ ::
#```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````




def get_embedding(face):
    # face = expand_dims(face, axis=0)
    embeddings = encodder.embeddings(np.array(face))
    return embeddings





#                                                      ──────▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
#                                                      ───▄▄██▌█  GUI screens
#                                                        ▄▄▄▌▐██▌█  in functions
#                                                       ███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄​▄▌
#                                                        ▀(@)▀▀▀▀▀▀▀(@)(@)▀▀▀▀▀▀▀▀▀▀▀▀(​@)▀▘ ::
#```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````




# login window
def launch_login_window():
    # layout =
    layout=[
         [sg.Text('Login', font=login_had1, pad=((5,5),(200,20)))],
         [sg.Text('User Name: ', font=login_had3, pad=login_pad, size=(16, 1)), sg.In(font=login_had3, size=(16,1))],
         [sg.Text('Password: ', font=login_had3, size=(16, 1), pad=login_pad), sg.In(password_char="*", size= (16,1), font=login_had3)],
         [sg.Button('Login', key="-LOGINBTN-", pad=login_pad, font=login_had4), sg.Button('Forget Password', key="-FORGET-", pad=login_pad, font=login_had4)],
         [sg.T("\n\n\n\nNot Registered?", font=h2, pad=login_pad)],
         [sg.Button("Register Now", key='-REGBTN-', font=login_had4, pad=login_pad), sg.Button('Exit', key="-LOGEXIT-", font=login_had4)]
    ]
    in_col=[[sg.Column(layout, element_justification="l", vertical_alignment="center")]]
    return sg.Window('Login - InViDet', in_col, location=(0,0), element_justification="c", size=screensize, finalize=True)

# register window
def launch_register_window():
    layout = [[sg.Text('Registration', font=login_had1, pad=((5,5), (200,20)))],
              [sg.T("\nEnter 8 digit product key", font=login_had4, pad=login_pad)],
              [sg.Input(size=(32,1),key='-PRDCT-', font=login_had3, pad=login_pad)],
              [sg.Button('Verify', pad=((5, 20), 10), font=login_had4, key="-VERIFY-")],
              [sg.T("Email", font=login_had3, size=(10, 1)),sg.Input(size=(16, 1), key='-EMAIL-', font=login_had3, pad=login_pad)],
              [sg.T("User Name", font=login_had3, size=(10,1)), sg.Input(size=(16,1),key='-SETUSERNAME-', font=login_had3, pad=login_pad)],
              [sg.T("Password", font=login_had3, size=(10,1)), sg.Input(size=(16,1),key='-SETPASS-', font=login_had3, pad=login_pad)],
              [sg.Button('Register', pad=((5,20),10), font=login_had4, key="-REGOK-")],
              [sg.Button('Login Now', key="-BKLOGIN-", font=login_had4, pad=login_pad), sg.Button('Exit', key="-REGEXIT-", font=login_had4, pad=login_pad)]]
    in_col=[[sg.Col(layout, element_justification="l", vertical_alignment="c")]]
    return sg.Window('Register - InViDet', in_col,location=(0,0), element_justification="c", size=screensize, finalize=True)

# main program window
def launch_main_window():

    title_layout = [[
        sg.Text('InVid Detector', justification='center', font=h1)
    ]]

    left_inputs_setting_col = [
        # picture_video_selection_layout
        [sg.T("Inputs", font=h2, pad=inputs_pad_standard, size= general_size)],
        [sg.T('Select Picture', pad=inputs_pad_standard, key="-SPIC-", size=(20, 1), font=h33),
         sg.In(key='-PICIN-', pad=inputs_pad_standard, visible=False),
         sg.FilesBrowse(target='-PICIN-', pad=inputs_pad_standard, key="-PBRS-", )],
        [sg.T('Select Video', pad=inputs_pad_standard, key="-SVID-", size=(20, 1), font=h33),
         sg.In(key='-VIDIN-', pad=inputs_pad_standard, visible=False),
         sg.FilesBrowse(target='-VIDIN-', pad=((5, 5), (2, 15)), disabled=False, key="-VBRS-", )],

        # input_details_layout
        [sg.T("Details on input", pad=setting_pad, font=h33, size=(24, 1))],
        [sg.T("Picture name: ", pad=setting_pad, font=h3, key="-PNAME-", size=(24, 1))],
        [sg.T("Video name: ", pad=setting_pad, font=h3, key="-VNAME", size=(24, 1))],
        [sg.T("Video frame rate: ", pad=setting_pad, font=h3, key="-VFPS-", size=(24, 1))],
        [sg.T("Video duration: ", pad=setting_pad, font=h3, key="-VDUR-", size=(24, 1))],

        # button for load
        [sg.B("Load Inputs", key="-LOAD-", pad=((5, 5), (1, 10))),
         sg.Radio("Cam Stream", "RADIO5", enable_events=True, font=h3, pad=(0, 0), size=(12, 1), key="-VIN1-"),
         sg.Radio("Video File", "RADIO5", enable_events=True, default=True, font=h3, pad=(0, 0), size=(12, 1),
                  key="-VIN2-")],

        # person_name_layout
        [sg.HSeparator()],
        [sg.T("Setting", font=h2, pad=setting_pad)],
        [sg.Text("Person Name", pad=setting_pad, font=h33),
         sg.Input(key="-PRNAME-", size=(10, 1), pad=setting_pad, font=h33, enable_events=True),
         sg.Text("(Optional)", pad=setting_pad, font=h3) ],

        # threshold_layout
        [sg.T("Threshold", pad=setting_pad, font=h33)],
        [sg.Radio('0.4', "RADIO1", size=(4, 1), pad=setting_pad, font=h3, key="-TH1-", enable_events=True),
         sg.Radio('0.5', "RADIO1", default=True, size=(4, 1), pad=setting_pad, font=h3, key="-TH2-", enable_events=True),
         sg.Radio('0.6', "RADIO1", size=(4, 1), pad=setting_pad, font=h3, key="-TH3-", enable_events=True),
         sg.Radio('0.7', "RADIO1", size=(4, 1), pad=setting_pad, font=h3, key="-TH4-", enable_events=True)],

        # verifying_layout
        [sg.T("Verifying Rate", pad=setting_pad, font=h33)],
        [sg.Radio("V1FPS", "RADIO2", default=True, font=h3, pad=setting_pad, size=(6, 1), key="-FPS1-", enable_events=True),
         sg.Radio("V2FPS", "RADIO2", font=h3, pad=setting_pad, size=(6, 1), key="-FPS2-", enable_events=True)],
        [sg.Radio("V3FPS", "RADIO2", font=h3, pad=setting_pad, size=(6, 1), key="-FPS3-", enable_events=True),
         sg.Radio("V4FPS", "RADIO2", font=h3, pad=setting_pad, size=(6, 1), key="-FPS4-", enable_events=True)],

        # write_video_layout
        [sg.T("Video Out", pad=setting_pad, font=h33)],
        [sg.Radio("No", "RADIO3", default=True, font=h3, pad=setting_pad, size=(6, 1), key="-VOUT1-", enable_events=True),
         sg.Radio("Yes", "RADIO3", font=h3, pad=setting_pad, size=(6, 1), key="-VOUT2-", enable_events=True)],
        [sg.T("Video Display", pad=setting_pad, font=h33)],
        [sg.Radio("No", "RADIO4", default=True, font=h3, pad=setting_pad, size=(6, 1), key="-VSHOW1-", enable_events=True),
         sg.Radio("Yes", "RADIO4", font=h3, pad=setting_pad, size=(6, 1), key="-VSHOW2-", enable_events=True)],

        # alarm
        [sg.T("Alarm On Recognition", pad=setting_pad, font=h33)],
        [sg.Radio("OFF", "RADIO6", default=True, font=h3, pad=setting_pad, size=(6, 1), key="-ALARM1-", enable_events=True),
         sg.Radio("ON", "RADIO6", font=h3, pad=setting_pad, size=(6, 1), key="-ALARM2-", enable_events=True)],

        # horisotal
        [sg.HSeparator()],
        # set_choice_layout
        [sg.T("Threshold\t: 0.5   (default)", pad=setting_pad, font=h3, key="-DFLT1-", size=(30, 1))],
        [sg.T("Verify Rate\t: 1FPS  (default)", pad=setting_pad, font=h3, key="-DFLT2-", size=(30, 1))],
        [sg.T("Video Out\t: NO    (default)", pad=setting_pad, font=h3, key="-DFLT3-", size=(30, 1))],
        [sg.T("Video Display\t: NO    (default)", pad=setting_pad, font=h3, key="-DFLT4-", size=(30, 1))],

        # aprx time to process
        [sg.T("Estimated time to process: ", pad=setting_pad, font=h3, key="-APRX-", size=(28, 1))],

        # buttons Start, logout, exit
        [sg.B("Start Processing", key='-START-', pad=setting_pad, font=h3, disabled=True),
         sg.B("Logout", key='-LOGOUT-', pad=setting_pad, font=h3),
         sg.B("Exit", key='-MAINEXIT-', pad=setting_pad, font=h3),
         sg.T("Error! Inputs Can't Load", font=h3, visible=False, key="-ERR-", text_color="red")]
    ]

    # right column that carry output logs
    right_col = [
        [sg.T("Output Logs", font=h2, pad=inputs_pad_standard)],
        [sg.Output(size=(output_width,output_height))]
    ]

    # middle column that carry Results
    mid_column = [
        [sg.T("Final Results", font=h2, pad=inputs_pad_standard)],
        [sg.T("Time Elapsed: ", visible=False, font=h3, key="-TIME-")],
        [sg.T("Results", key="-RES-", size=(output_width,result_height), font=h3)],
        [sg.B("Show Results", key="-SHOW-", font=h3), sg.B("Clear Results", key="-CLEAR-", font=h3)]
    ]

    # final layout/ integrated layout
    layout = [
        [sg.Column(title_layout, element_justification='center', pad=((int(width/2-150), 0), 1))],
        [sg.HSeparator()],
        [sg.Column(left_inputs_setting_col, element_justification="left", size=(int(width/3-150),height)), sg.VSeperator(),
         sg.Col(mid_column, element_justification="left", size=(int(width/3),height)), sg.VSeperator(),
         sg.Column(right_col, element_justification="left", size=(int(width/3),height))]
    ]

    # starting windows
    print("[INFO] Launching main winow")
    return sg.Window('Home - InViDet', layout, location=(0,0), size=screensize, finalize=True)





#                                                      ──────▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
#                                                      ───▄▄██▌█  Launching 1st window
#                                                        ▄▄▄▌▐██▌█  and HANDLING EVENTS
#                                                       ███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄​▄▌
#                                                        ▀(@)▀▀▀▀▀▀▀(@)(@)▀▀▀▀▀▀▀▀▀▀▀▀(​@)▀▘ ::
#```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````

# start off with 1 window open
login_window, register_window, main_window = launch_login_window(), None, None



# Event Loop
while True:
    window, event, values = sg.read_all_windows()

    # handling when exit button clicked or closing window
    if event == sg.WIN_CLOSED or event in ["-LOGEXIT-" ,"-REGEXIT-", "-MAINEXIT-"]:

        if window == register_window:
            window.close()
            register_window = None

        if window == main_window:
            window.close()
            main_window = None

        if window == login_window:
            login_window = None
            window.close()

        # finally exit program in any case
        exit()

    # taking control to main window, if successfully login
    if event == "-LOGINBTN-" and not register_window and not main_window:
        main_window = launch_main_window()
        login_window.close()
        login_window = None
        register_window = None

    # handling popup event if clicked forget password
    if event == "-FORGET-":
        email = sg.popup_get_text('Enter your email address', 'Forget Password', size=(20,3), font=login_had4)
        sg.popup('Password Recovery', 'Instructions to recover are sent to', email)

    # taking control to Registration screen, when clicked register now
    if event == '-REGBTN-' and not register_window and not main_window:
        register_window = launch_register_window()
        login_window.close()
        login_window = None
        main_window = None

    # taking back to login screen, clicked login now, from register screen
    if event == "-BKLOGIN-" and not login_window and not main_window:
        login_window = launch_login_window()
        register_window.close()
        register_window = None
        main_window = None

    # taking control back to login window, if successfully registered
    if event == "-REGOK-":
        login_window = launch_login_window()
        register_window.close()
        register_window = None
        main_window = None

    # taking control back to login window, if logout, from main window
    if event == "-LOGOUT-":
        login_window = launch_login_window()
        main_window.close()
        register_window = None
        main_window = None



#                                                      ──────▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
#                                                      ───▄▄██▌█  Load inputs
#                                                        ▄▄▄▌▐██▌█  in HANDLING EVENTS
#                                                       ███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄​▄▌
#                                                        ▀(@)▀▀▀▀▀▀▀(@)(@)▀▀▀▀▀▀▀▀▀▀▀▀(​@)▀▘ ::
#```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````




    # handling video source choice
    # if cam stream
    if event == "-VIN1-":
        if video_source_changing == 1:
            continue        # doing it so that it wont monitor every click, only monitor first click to cam stream or video file


        # emptying video variable as well as video input sources when it clicked second time,
        # coming back from cam stream, to specifically asked the user to select new video
        # dont rely on previous video choices
        video_input=""
        window["-VIDIN-"].update("")
        video_file=False
        print("[INFO] Video source changed to Cam Stream")
        window["-SVID-"].update("Select Video")
        window["-VNAME"].update(value="Video name: ")
        window["-VFPS-"].update(value="Video frame rate:" )
        window["-VDUR-"].update(value="Video duration: ")
        window["-VBRS-"].update(disabled=True)
        try:
            cam = cv2.VideoCapture(0)
            fps = int(cam.get(5))
            print("fps:", fps)
            cam.release()
            cv2.destroyAllWindows()
        except:
            print("[ERROR] Live Stream is unable to read")
            print("[ERROR] Permission Denied!")
            break

        video_source_changing=1
        # if cam stream it should be able to perform, dont wait for video input as
        # source has changed to cam stream and picture is loaded
        # start button now enabled
        if not video_file and len(picture_input)>0:
            window["-START-"].update(disabled=False)

    # if video file
    if event == "-VIN2-":
        if video_source_changing == 0:
            continue        # doing it so that it wont monitor every click, only monitor first click to cam stream or video file

        # start became disabled again if no source video, unless there is video file loaded
        if video_input == "":
            window["-START-"].update(disabled= True)
        video_file=True
        print("[INFO] Video source changed to video file on disc")
        window["-VBRS-"].update(disabled=False)
        video_source_changing=0

    # load button, it verify extension and fill the address carrying variables picture_input or video_input
    if event == '-LOAD-':
        picture_input = values["-PICIN-"]
        video_input = values["-VIDIN-"]
        window.refresh()
        # if brows button returned some string of address, it length would be greater than 0
        if len(picture_input) > 0:
            image_extension = picture_input.rsplit(".", 1)[1]
            # check on extension
            if image_extension not in ["tif", "tiff", "bmp", "jpg", "jpeg", "gif", "png", "esp"]:
                print(
                    "[ERROR] Image file extension is not known\n[ERROR] Check Image path, chose again with known image\n[ERROR] extensions instead of .%s" % image_extension)
                window["-SPIC-"].update("Picture Error")
                continue

            print("[INFO] Picture is loaded")
            window["-SPIC-"].update("Picture SELECTED")
            pic_name = picture_input.rsplit("/", 1)
            pic_name = "Picture name: %s" % pic_name[1]
            window["-PNAME-"].update(value=str(pic_name))
        else:
            print("[WARN] Picture is MISSING")
        window.refresh()
        if len(video_input) > 0:

            video_extension = video_input.rsplit(".", 1)[1]
            # check on extension
            if video_extension not in ["mp4", "MP4", "MOV", "mov", "WMV", "wmv", "FLV", "flv", "AVI", "avi",
                                       "AVCHD", "avchd", "WebM", "webm", "MKV", "mkv"]:
                print(
                    "[ERROR] Video file extension is not known\n[ERROR] Check Video path, chose again with known Video\n"
                    "[ERROR] extensions instead of .%s" % video_extension)
                window["-SVID-"].update("Video Error")
                continue

            print("[INFO] Video is loaded")
            window["-SVID-"].update("Video SELECTED")
            # obtaining fps and setting text

            vid_url = video_input.rsplit("dett", 1)
            vid_url = vid_url[1][1:]
            # print(vid_url)
            cap = cv2.VideoCapture(vid_url)
            fps = int(cap.get(5))
            print("[INFO] fps of selected video", fps)
            frame_count = int(cap.get(7))
            cap.release()
            cv2.destroyAllWindows()
            print("[INFO] Total frames of selected video", frame_count)
            # clip= VideoFileClip(vid_url)
            # duration= clip.duration
            sec = int(frame_count / fps)
            min = int(sec / 60)
            sec = int(sec % 60)
            hr = int(min / 60)
            min = int(min % 60)
            # int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # getting/setting estimated duration
            video_duration_string = "Video duration: " + str(hr) + ":" + str(min) + ":" + str(sec)
            est_sec = int(frame_count / fps * aprx_ratio + 10)
            est_min = int(est_sec / 60)
            est_sec = int(est_sec % 60)
            est_hr = int(est_min / 60)
            est_min = int(est_min % 60)
            estimated_time_string = "Estimated time to process: " + str(est_hr) + ":" + str(est_min) + ":" + str(
                est_sec)
            window["-APRX-"].update(estimated_time_string)

            # if time_s > 60:
            #     time_m = time_s / 60
            #     window["-APRX-"].update("Estimated time to process: %s min" % str(time_m)[0:4])
            #     if time_m > 60:
            #         time_h = time_m / 60
            #         window["-APRX-"].update("Estimated time to process: %s hour" % str(time_h)[0:4])

            vid_name = vid_url.rsplit("/", 1)
            # print(vid_name, pic_url)
            vid_name = f'{"Video name: "}{vid_name[1]}'
            message_fps = "Video frame rate: %s" % fps
            # print(vid_name, fps, pic_url)
            # window.refresh()
            window["-VNAME"].update(value=vid_name)
            window["-VFPS-"].update(value=message_fps)
            window["-VDUR-"].update(value=video_duration_string)
        else:
            # start button back to disabled if video input missing
            if video_file:
                window["-START-"].update(disabled=True)
                print("[WARN] Video is MISSING")
        # window.refresh()

        if len(picture_input) > 0 and len(video_input) > 0:
            print("[INFO] Inputs are loaded successfully")
            window["-START-"].update(disabled=False)
            window["-ERR-"].update(visible=False)
            window.refresh()
        if not video_file and len(picture_input) > 0:
            print("[INFO] Inputs are loaded successfully")
            window["-START-"].update(disabled=False)
            window["-ERR-"].update(visible=False)
            window.refresh()






#                                                      ──────▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
#                                                      ───▄▄██▌█  Setting
#                                                        ▄▄▄▌▐██▌█  in HANDLING EVENTS
#                                                       ███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄​▄▌
#                                                        ▀(@)▀▀▀▀▀▀▀(@)(@)▀▀▀▀▀▀▀▀▀▀▀▀(​@)▀▘ ::
# ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````




    # handling threshold choices
    if event== "-TH1-":
        window["-DFLT1-"].update("Set Threshold\t: 0.4")
        threshold = 0.4
        print("[INFO] Thresholds: ", threshold)
    if event == "-TH2-":
        window["-DFLT1-"].update("Set Threshold\t: 0.5   (default)")
        threshold = 0.5
        print("[INFO] Thresholds: ", threshold)

    if event == "-TH3-":
        window["-DFLT1-"].update("Set Threshold\t: 0.6")
        threshold = 0.6
        print("[INFO] Thresholds: ", threshold)
    if event == "-TH4-":
        window["-DFLT1-"].update("Set Threshold\t: 0.7")
        threshold = 0.7
        print("[INFO] Thresholds: ", threshold)


    # setting vfps
    if event == "-FPS1-":
        window["-DFLT2-"].update("Verify Frame Rate\t: 1FPS  (default)")
        # updating time estomation based on choice
        aprx_ratio = 0.75
        est_sec = int(frame_count / fps * aprx_ratio + 10)
        est_min = int(est_sec / 60)
        est_sec = int(est_sec % 60)
        est_hr = int(est_min / 60)
        est_min = int(est_min % 60)
        estimated_time_string = "Estimated time to process: " + str(est_hr) + ":" + str(est_min) + ":" + str(est_sec)
        window["-APRX-"].update(estimated_time_string)

        # setting verifying fps
        v_fps = 1
        print("[INFO] FPS: ", v_fps)
        print("[INFO] Estimated time to process: ", (duration* aprx_ratio)+10, "seconds")    # 0.75 is ratio on my pc for v1FPS +10 tensor flow loading delay

    if event == "-FPS2-":
        window["-DFLT2-"].update("Verify Frame Rate\t: 2FPS")
        # updating time estomation based on choice
        aprx_ratio = 1.5
        est_sec = int(frame_count / fps * aprx_ratio + 10)
        est_min = int(est_sec / 60)
        est_sec = int(est_sec % 60)
        est_hr = int(est_min / 60)
        est_min = int(est_min % 60)
        estimated_time_string = "Estimated time to process: " + str(est_hr) + ":" + str(est_min) + ":" + str(est_sec)
        window["-APRX-"].update(estimated_time_string)

        # setting verifying fps
        v_fps = 2
        print("[INFO] FPS: ", v_fps)
        print("[INFO] Estimated time to process: ", (duration* aprx_ratio)+10, "seconds")    # 0.75 is ratio on my pc for v1FPS +10 tensor flow loading delay


    if event == "-FPS3-":
        window["-DFLT2-"].update("Verify Frame Rate\t: 3FPS")
        # updating time estomation based on choice
        aprx_ratio = 2.25
        est_sec = int(frame_count / fps * aprx_ratio + 10)
        est_min = int(est_sec / 60)
        est_sec = int(est_sec % 60)
        est_hr = int(est_min / 60)
        est_min = int(est_min % 60)
        estimated_time_string = "Estimated time to process: " + str(est_hr) + ":" + str(est_min) + ":" + str(est_sec)
        window["-APRX-"].update(estimated_time_string)

        # setting verifying fps
        v_fps = 3
        print("[INFO] FPS: ", v_fps)
        print("[INFO] Estimated time to process: ", (duration* aprx_ratio)+10, "seconds")    # 0.75 is ratio on my pc for v1FPS +10 tensor flow loading delay


    if event == "-FPS4-":
        window["-DFLT2-"].update("Verify Frame Rate\t: 4FPS")
        # updating time estomation based on choice
        aprx_ratio = 3
        est_sec = int(frame_count / fps * aprx_ratio + 10)
        est_min = int(est_sec / 60)
        est_sec = int(est_sec % 60)
        est_hr = int(est_min / 60)
        est_min = int(est_min % 60)
        estimated_time_string = "Estimated time to process: " + str(est_hr) + ":" + str(est_min) + ":" + str(est_sec)
        window["-APRX-"].update(estimated_time_string)

        # setting verifying fps
        v_fps = 4
        print("[INFO] FPS: ", v_fps)
        print("[INFO] Estimated time to process: ", (duration* aprx_ratio)+10, "seconds")    # 0.75 is ratio on my pc for v1FPS +10 tensor flow loading delay



    # setting video write options
    if event == "-VOUT1-":
        window["-DFLT3-"].update("Write Video\t: NO    (default)")
        v_out = False
        print("[INFO] Video OUT: ", v_out)

    if event == "-VOUT2-":
        window["-DFLT3-"].update("Write Video\t: YES")
        v_out = True
        print("[INFO] Video OUT: ", v_out)


    # setting Video show options
    if event == "-VSHOW1-":
        window["-DFLT4-"].update("Show Video\t: NO    (default)")
        v_show = False
        print("[INFO] Video SHOW: ", v_show)

        # showing video may cause a little delay so updating it
        est_sec = int(frame_count / fps * aprx_ratio + 10)
        est_min = int(est_sec / 60)
        est_sec = int(est_sec % 60)
        est_hr = int(est_min / 60)
        est_min = int(est_min % 60)
        estimated_time_string = "Estimated time to process: " + str(est_hr) + ":" + str(est_min) + ":" + str(est_sec)
        window["-APRX-"].update(estimated_time_string)

    if event == "-VSHOW2-":
        window["-DFLT4-"].update("Show Video\t: YES")
        v_show = True
        print("[INFO] Video SHOW: ", v_show)

        # showing video may cause a little delay so updating it
        est_sec = int(frame_count / fps * aprx_ratio *1.05 + 10)
        # 1.05 approximately delay ratio for showing vs not showing
        est_min = int(est_sec / 60)
        est_sec = int(est_sec % 60)
        est_hr = int(est_min / 60)
        est_min = int(est_min % 60)
        estimated_time_string = "Estimated time to process: " + str(est_hr) + ":" + str(est_min) + ":" + str(est_sec)
        window["-APRX-"].update(estimated_time_string)


    # setting person name
    if event == "-PRNAME-":
        person_name= window["-PRNAME-"].get()
        print("\n[INFO] Person name changed")





    # opening result text file in default editor
    if event == "-SHOW-":
        # OS dependent for windows use OS library
        # os.system("Final_Results_Invidet.txt")
        subprocess.call(["xdg-open", "Final_Results_Invidet.txt"])





#                                                      ──────▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
#                                                      ───▄▄██▌█  Start Process
#                                                        ▄▄▄▌▐██▌█  in HANDLING EVENTS
#                                                       ███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄​▄▌
#                                                        ▀(@)▀▀▀▀▀▀▀(@)(@)▀▀▀▀▀▀▀▀▀▀▀▀(​@)▀▘ ::
# ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````



    if event == "-START-":
        if len(picture_input)<1:
            print("[ERROR] Picture is not loaded yet")
            window["-ERR-"].update(visible=True)
            continue
        else:
            window["-ERR-"].update(visible=False)

        if video_file and len(video_input)<1:
            print("[ERROR] Video is not loaded yet")
            window["-ERR-"].update(visible=True)
            continue
        else:
            window["-ERR-"].update(visible=False)

        window.refresh()

#__________________________________________________Internal Condition Where main logic on Start process actually start______________________________

        if len(picture_input)>0 and (len(video_input)>0 or video_file==False):
            if first>0:
                window["-RES-"].update("Fetching new results")
                print("[INFO] Fetching results for the ", first, " time")
                first+= 1
            else:
                first += 1
                print("[INFO] Fetching results for the ", first, " time")
            print("[INFO] Starting process!")
            print("[INFO] 10s delay on loading TensorFlow")

            # to monitor how much time it took
            process_start = times.now()




# __________________________________________________Break Point Start_____________________________________________________________________________________
            # break point its initial where integration started for one_main_V3

            # below call is no more needed
            # track_records= compare_faces(picture_input, video_input, fps, threshold, v_fps, person_name, v_out, v_show, video_file)

            # beloe is original compare function defination was this from face_compare module
            #def compare_faces(pic_url, vid_url, fps, threshold, v_fps, person_name, v_out, v_show, video_file):

            print("[INFO] Start processing")


            # checking it is a cam stream, if it is, setting fps by self, not relying on cv2 to get fps from video file or else it raised exception modulo by zero
            # bug fix 1.4
            #
            # second thoughts, No more need this bug fix as fps is being set for cam stream at the time
            # changing video source option in event => VIN1 at line #380
            # if video_file == False:
            #     fps = 30


            # setting divisibe and tolerance based on vfps choice
            print("[INFO] Calculating divisible based on suitable tolerance...")
            if v_fps == 1:
                divisible = fps
                tolerance = 2
            if v_fps == 2:
                tolerance = 3
                divisible = fps / 2
            if v_fps == 3:
                tolerance = 4
                divisible = fps / 3
            if v_fps == 4:
                tolerance = 5
                divisible = fps / 4
            print("[INFO] Tolerance set to ", tolerance, " to tolerate miss match")
            print("[INFO] Divisible set to", divisible, "based on verifying frame rate")

            try:
                # slicing path string because folder reside in project directory
                pic_url = picture_input.rsplit("InVidett/", 1)
                pic_url = pic_url[1]
                picture_name = pic_url.rsplit("/", 1)[1][0:5]
                output_video_name = person_name + "-" + picture_name
            except:
                print("[ERRO] Picture was unable to load")
                break

            # second thoughts; as facenet was failing at embedding for alligned face
            # it must be due to backend operations and self alignment at some point; no more needed face alignment

            # getting aligned face
            # pic_face= extract_align_face(pic_url)       #pic_face is aligned np array of face
            # print(pic_url)


            print("[INFO] Started face extraction from picture input")
            try:
                pic_face_array = np.array(Image.open(pic_url))
                pic_face = encodder.extract(pic_url)
                pic_face = pic_face[0]['box']
                x1, y1, width, height = pic_face
                x2, y2, = x1 + width, y1 + height
                pic_face = pic_face_array[y1:y2, x1:x2]
            except:
                print("[ERROR] couldn't get face on picture")
                continue


            print("[INFO] Successfully extracted face from picture input")

            # expanding dimensions for facenet; kind of normalizing
            pic_face = expand_dims(pic_face, axis=0)
            try:
                pic_embeddings = encodder.embeddings(np.array(pic_face))
            except:
                print("[ERROR] Couldn't get embedding on picture")
                break

            # initializing list() to track frames
            tracked_list = list()

            # making sure video is writeable specifying or declaring early width and heights
            width = 640
            height = 480
            # size = tuple((640,480))
            if video_file:
                try:
                    vid_url = video_input.rsplit("InVidett", 1)
                    video_name = str(vid_url).rsplit("/", 1)[1][0:5]
                    output_video_name = output_video_name + "-" + video_name
                    vid_url = vid_url[1][1:]
                    cap = cv2.VideoCapture(vid_url)
                    width = int(cap.get(3))
                    height = int(cap.get(4))
                    fps = int(cap.get(5))
                    print("[INFO] Video file is successfully loaded")
                    print("[INFO] details video: resolutions:", (width, height), " fps:", fps)

                    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) +25       # this plus 25 is what cv2 count less at average from bigger and smaller videos

                except:
                    print("[ERROR] Video is unable to load, check path")
                    tracked_list = ["ERROR"]
                    break
                    # return tracked_list
            else:
                try:
                    cap = cv2.VideoCapture(0)
                    print("[INFO] Cam video is successfully linked")

                    width = int(cap.get(3))
                    height = int(cap.get(4))
                    fps = int(cap.get(5))
                    # print("(w,h", (width,height))
                    output_video_name = output_video_name + "-onLiveCam"
                except:
                    print("[ERROR] Cam is unable to load, check permission")
                    tracked_list = ["ERROR"]
                    break
                    # return tracked_list

            # if video write option is true; then write
            if v_out:
                print("[INFO] Video write option is set TRUE, initializing")
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                # if video_file:
                # size= tuple((width, height))
                output_video_url = "pic_input/" + output_video_name + ".avi"
                out = cv2.VideoWriter(output_video_url, fourcc, v_fps, (width, height))  # (640, 480))
                print("[INFO] Output video path is set to:",output_video_url)

            # initializing frame counts
            countframes = 0

            # to serialize generated results at runtime; may be used in some conditions too
            runtime_find = 1

            # initializing result string to carry and wirte results in the end also to update final results middle column at runtime
            result_string = ""

            # variable is part of logic later to only show result one time one it reached to 15 results
            has_shown_final_message = False

            # initializing as a part of logic for tracking
            first_marked_frame, last_marked_frame, not_matched, outer_no_face, match = 0, 0, 0, 0, 0

            # it always true unless video has no more frames, or exception raised at some point.
            while True:
                try:
                    ret, frame = cap.read()
                    countframes += 1
                except:
                    print("[WARN] URL/selection for the video file is not valid:", vid_url)
                    print("[ERROR] Could not load anymore frames")
                    break

                # divisible is based on user verifying frame rate per seconds
                # so it is only go further than this condition if it is desired frame
                if countframes % int(divisible) != 0:
                    continue

                # because openCV return image in BGR format in cap.read()
                # has to convert it back to RGB which is prefered in FaceNET and MTCNN
                try:
                    rgb_frame = frame[:, :, ::-1]
                    frame_array = np.array(rgb_frame)
                except:
                    # bug fix 1.3
                    # it cant convert frame to rgb when cap.read() return None in frame
                    print("[WARN] Got nothing in frame variable coming from openCV, frame=", frame)
                    print("[ERROR] Video file is corrupted or has no more frames, total frames= ", countframes)
                    break

                # loading detector from MTCNN
                # detector = MTCNN()
                # saving all faces in faces; a call to facenet encodder extract function
                faces = encodder.extract(rgb_frame)

                # if it return some faces in current frame; then len(faces) must be greater than one, only then go further
                if len(faces) > 0:
                    print('[INFO] Found %s faces in frame no: ' % len(faces), countframes)

                    # initializing to check frames with no faces
                    outer_no_face = 0

                    # taking variable face_num; to iterate in loop; for detecting multiple faces in single frame
                    face_num = 0

                    for face in faces:
                        # starting point coordinates of face are being stored in x1, y1, against each face it returns a dictionary
                        # dictionary 'box' contain a bounding box which return starting points and from these points a width from x and
                        # a height y
                        x1, y1, width, height = faces[face_num]['box']

                        # storing ending points in x2, y2
                        x2, y2, = x1 + width, y1 + height

                        # extracting current face from frame_array; frame array is whole image or array; we want to extract that single face
                        frame_face = frame_array[y1:y2, x1:x2]

                        # expanding dimensions to normalize it for facenet
                        frame_face = expand_dims(frame_face, axis=0)

                        # increasing face number to extract the next face 'BOX' in current frame; for the next coming iteration if it is
                        face_num += 1

                        # bug fix
                        # at testing while getting embedding it raised exception, says in resize function of FaceNet
                        # so it couldn't get embedding sometime; we dont want to break the program; so continue the loop
                        try:
                            frame_face_embeddings = get_embedding(frame_face)
                        except:
                            print("[WARN] Exception raised")
                            print("[WARN] Could not get embedding for frame no:", countframes, "/", total_frames)
                            continue

                        # getting distance through cosine
                        distance = cosine(pic_embeddings, frame_face_embeddings)

                        # used threshold provided by user from GUI;in our contion
                        # if not under threshold
                        if distance >= threshold:
                            recognised = False
                            if not video_file:
                                print("[INFO] Match is False for face", face_num, "/", len(faces), "with the distance", str(distance)[0:3], "in the frame",
                                      countframes, "/", countframes)
                            else:
                                print("[INFO] Match is False for face", face_num, "/", len(faces), "with the distance", str(distance)[0:3], " in the frame",
                                      countframes, "/", total_frames)
                        # if in threshold range
                        else:
                            recognised = True
                            if not video_file:
                                print("[INFO] Match is True for face", face_num, "/", len(faces), "with the distance", str(distance)[0:3], " in the frame",
                                      countframes, "/", countframes)
                            else:
                                print("[INFO] Match is True for face", face_num, "/", len(faces), "with the distance", str(distance)[0:3], " in the frame",
                                      countframes, "/", total_frames)

                            print("[INFO] Saving tracks for current frame", countframes)
                            print("[INFO]", person_name, "found with the distance", str(distance)[0:5])

                        # logic when face is recognised; its kind of complex here
                        if recognised == True:
                            match += 1
                            # if video is being displayed or being writen
                            if v_show or v_out:
                                message1 = "[Current Frame: " + str(countframes) + "/" + str(total_frames) + "]"
                                message3 = "[" + person_name + "]" + " , [DISTANCE: " + str(distance)[0:4] + "]"
                                sec = countframes / fps
                                min = int(sec / 60)
                                sec = int(sec % 60)
                                hr = int(min / 60)
                                min = int(min / 60)

                                message2 = "[Aprx Time: " + str(hr) + ":" + str(min) + ":" + str(sec) + "]"

                                # if its a live stream; then putting different text on frame
                                if not video_file:
                                    current_time = times.now()
                                    message2 = "[Live Time: " + str(current_time)[11:19] + "]"
                                    message1 = "[     Date: " + str(current_time)[0:10] + "]"
                                # "y"; show name upper side of bounding box if there is space if no space left show towards donside
                                ms3 = y1 - 10 if y1 - 10 > 10 else y1 + 10
                                ms2 = y1 - 25 if y1 - 25 > 25 else y1 + 25
                                ms1 = y1 - 40 if y1 - 40 > 40 else y1 + 40

                                # drawing rectangle around the face points stored in x1,y1, x2,y2
                                cv2.rectangle(frame_array, (x1, y1), (x2, y2), (155, 25, 25), 2)
                                # putting text on bounding box
                                cv2.putText(frame_array, message1, (x1, ms1), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                                            (155, 25, 25), 2)
                                cv2.putText(frame_array, message2, (x1, ms2), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                                            (155, 25, 25), 2)
                                cv2.putText(frame_array, message3, (x1, ms3), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                                            (155, 25, 25), 2)

                            # marking first frame; in which face was recognized
                            if match == 1:
                                # if video file;
                                if video_file:
                                    first_marked_frame = countframes
                                    print("[INFO] First Match at frame: ", countframes, "/", total_frames)

                                    # adjusting time
                                    start_time_seconds = int(countframes / fps)
                                    start_time_mins = int(start_time_seconds / 60)
                                    start_time_seconds = int(start_time_seconds % 60)
                                    start_time_hour = int(start_time_mins / 60)
                                    start_time_mins = int(start_time_mins % 60)

                                    # only for 15 results
                                    if runtime_find <= 15:
                                        result_string = result_string + str(
                                            runtime_find) + ". Match start at frame no: " + str(
                                            countframes) + ", at time: " + str(start_time_hour) + ":" + str(
                                            start_time_mins) + ":" + str(start_time_seconds) + "\n"
                                        window["-RES-"].update(result_string)

                                    else:
                                        if not has_shown_final_message:
                                            has_shown_final_message = True
                                            result_string = result_string + "\n" + "Showing only first 15 results for more click on show results once process finished\ntotal results so far: " + str(
                                                runtime_find)
                                            window["-RES-"].update(result_string)


                                # if cam stream
                                    # print("[INFO] First Match at frame: ", countframes, "/", countframes)
                                    # result_string_list.append(str(runtime_find)+". Match start at frame no: "+str(countframes)+", at time: "+str(times.now()))
                                    # updating result run time
                                else:
                                    first_marked_frame = countframes
                                    tracked_list.append(str(runtime_find) + ". Match start at frame no: " + str(
                                        countframes) + ", at time: " + str(times.now())[0:20]+"\n")

                                    print("[INFO] Match Start at frame no:", first_marked_frame, "/", countframes)

                                    # only for first 15 results should show
                                    if runtime_find <= 15:
                                        result_string = result_string + str(
                                            runtime_find) + ". Match start at frame no: " + str(
                                            countframes) + ", at time: " + str(times.now())[0:20] + "\n"
                                        window["-RES-"].update(result_string)
                                        # for res in result_string:
                                        #     result_string = result_string + res + "\n"

                                    else:
                                        # only show the message 1 time
                                        if not has_shown_final_message:
                                            # print("[INFO] Last Match at frame: ", last_marked_frame, "/", countframes)
                                            has_shown_final_message = True
                                            result_string = result_string + "\n" + "Showing only first 15 results for more click on show results once process finished\ntotal results so far: " + str(
                                                runtime_find)
                                            window["-RES-"].update(result_string)

                                runtime_find += 1


                            not_matched = 0
                            print("[INFO] Match is True for frame: ", first_marked_frame, " to ", countframes)
                            break

                        else:
                            # logic when face is not matched, tolerance tells how much to tolerate this behaviour
                            not_matched += 1
                            # adding length of faces too, because if there are too many faces tolerate will fail, if alone,
                            # Doubt not tested yet, but it seems so
                            if not_matched == (tolerance * len(faces)):
                                if first_marked_frame > 0:
                                    if not video_file:
                                        last_marked_frame = int(countframes - (tolerance * divisible))
                                        tracked_list.append(
                                            "Match end at frame no: " + str(countframes) + ", at time: " + str(
                                                times.now())[0:20]+"\n")
                                        print("[INFO] Last Match at frame: ", last_marked_frame, "/", countframes)
                                        # updating result run time
                                        if runtime_find<=15:
                                            result_string = result_string +"    Match end at frame no: " + str(
                                                last_marked_frame) + ", at time: " + str(times.now())[0:20] + "\n"
                                            window["-RES-"].update(result_string)
                                        else:
                                            if not has_shown_final_message:
                                                has_shown_final_message= True
                                                result_string = result_string + "\n" + "Showing only first 15 results for more click on show results once process finished\ntotal results so far: " + str(
                                                    runtime_find)
                                                window["-RES-"].update(result_string)

                                    else:
                                        last_marked_frame = int(countframes - (tolerance * divisible))
                                        print("[INFO] Last Match at frame: ", countframes, "/", total_frames)

                                        # adjusting time
                                        end_time_seconds = int(last_marked_frame / fps)
                                        end_time_mins = int(end_time_seconds / 60)
                                        end_time_seconds = int(end_time_seconds % 60)
                                        end_time_hour = int(end_time_mins / 60)
                                        end_time_mins = int(end_time_mins % 60)

                                        # showing only first 15 results
                                        if runtime_find<=15:
                                            result_string=result_string + "    Match end at frame no: " + str(
                                                countframes) + ", at time: " + str(end_time_hour) + ":" + str(
                                                end_time_mins) + ":" + str(end_time_seconds)+"\n"
                                            window["-RES-"].update(result_string)
                                        else:
                                            if not has_shown_final_message:
                                                has_shown_final_message= True
                                                result_string = result_string + "\n" + "Showing only first 15 results for more click on show results once process finished\ntotal results so far: " + str(
                                                    runtime_find)
                                                window["-RES-"].update(result_string)


                                        # appending frames in track_list; so tha later it could be used to extract exact time
                                        # second thoughts logic can be changed here
                                        # notes: if it follow the same approach used for live cam i.e. saving direct strings
                                        #        things would become easy at the end where you read tracked_list and you
                                        #        dont need to extracting indexes to pull results; complexity will decrease
                                        #        greatly
                                        tracked_list.append(first_marked_frame)
                                        tracked_list.append(last_marked_frame)


                                    # bug fix, get to outer of vid source selection
                                    first_marked_frame = 0
                                    last_marked_frame = 0
                                    match = 0
                                    print("[INFO] Last Match at frame: ", countframes - (tolerance * divisible))


                else:
                    # logic when no face is found in current frame
                    outer_no_face += 1
                    if outer_no_face == tolerance:
                        if first_marked_frame > 0:
                            if not video_file:
                                # first_marked_frame = countframes
                                last_marked_frame = int(countframes - (tolerance * divisible))
                                tracked_list.append(
                                    "Match end at frame no: " + str(countframes) + ", at time: " + str(
                                        times.now())[0:20]+"\n")
                                print("[INFO] Last Match at frame: ", last_marked_frame, "/", countframes)
                                if runtime_find <= 15:
                                    result_string = result_string + "    Match end at frame no: " + str(
                                        last_marked_frame) + ", at time: " + str(times.now())[0:20] + "\n"
                                    window["-RES-"].update(result_string)
                                else:
                                    if not has_shown_final_message:
                                        has_shown_final_message = True
                                        result_string = result_string + "\n" + "Showing only first 15 results for more click on show results once process finished\ntotal results so far: " + str(
                                            runtime_find)
                                        window["-RES-"].update(result_string)

                            else:
                                last_marked_frame = int(countframes - (tolerance * divisible))

                                print("[INFO] Last Match at frame: ", countframes, "/", total_frames)
                                end_time_seconds = int(last_marked_frame / fps)
                                end_time_mins = int(end_time_seconds / 60)
                                end_time_seconds = int(end_time_seconds % 60)
                                end_time_hour = int(end_time_mins / 60)
                                end_time_mins = int(end_time_mins % 60)

                                if runtime_find <= 15:
                                    result_string = result_string + "    Match end at frame no: " + str(
                                        countframes) + ", at time: " + str(end_time_hour) + ":" + str(
                                        end_time_mins) + ":" + str(end_time_seconds) + "\n"
                                    window["-RES-"].update(result_string)
                                else:
                                    if not has_shown_final_message:
                                        has_shown_final_message = True
                                        result_string = result_string + "\n" + "Showing only first 15 results for more click on show results once process finished\ntotal results so far: " + str(
                                            runtime_find)
                                        window["-RES-"].update(result_string)

                                # appending frames in track_list; so tha later it could be used to extract exact time
                                # second thoughts logic can be changed here
                                # notes: if it follow the same approach used for live cam i.e. saving direct strings
                                #        things would become easy at the end where you read tracked_list and you
                                #        dont need to extracting indexes to pull results; complexity will decrease
                                #        greatly
                                tracked_list.append(first_marked_frame)
                                tracked_list.append(last_marked_frame)

                            first_marked_frame = 0
                            last_marked_frame = 0
                            match = 0
                            print("[INFO] Last Match at frame: ", countframes - (tolerance * divisible))



                        # append in face list
                        # faces_list.append(frame_face)

                if video_file:
                    print("[INFO] Total frames processed: ", countframes, "/", total_frames)
                else:
                    print("[INFO] Total frames processed: ", countframes, "/", countframes)
                # just for test purpose limiting frames, it was at initial testing
                # if countframes >= 130:
                #     break

                # only write current frame if v_out is true
                if v_out:
                    if video_file:
                        print("[INFO] Writing frame ", countframes, "/", total_frames, " in output video")
                    else:
                        print("[INFO] Writing frame ", countframes, "/", countframes, " in output video")

                    out.write(frame_array[:, :, ::-1])
                    # if cv2.waitKey(0) & 0xFF == ord('q'):
                    #     break
                    # cv2.waitKey(1)

                # only show if it sets true
                if v_show:
                    if video_file:
                        print("[INFO] Showing frame ", countframes, "/", total_frames)
                    else:
                        print("[INFO] Showing frame ", countframes, "/", countframes)
                    cv2.imshow("InVidet", frame_array[:, :, ::-1])
                    # ideal is waitkey(0), but (1) is working for me
                    # cv2.waitKey(1)
                    if cv2.waitKey(2) & 0xFF == ord('q'):
                        break

            # for last verified  frame, if it is not tracked
            if first_marked_frame > 0:
                last_marked_frame = countframes
                tracked_list.append(first_marked_frame)
                tracked_list.append(last_marked_frame)
                if video_file:
                    print("[INFO] Final Matched frame: ", countframes, "/", total_frames)
                else:
                    print("[INFO] Final Matched frame: ", countframes, "/", countframes)
                # print("[INFO] Returning tracked list back to GUI")

            # releasing video and destroying windows
            cap.release()
            # releasing out if initialized
            if v_out:
                out.release()
            cv2.destroyAllWindows()

# __________________________________________________Break Point End_____________________________________________________________________________________







            # extracting current starting time with current tiem to get the total elapsed time
            process_elapsed_time = times.now() - process_start

            # now if tracked_list have some results
            if len(tracked_list) >0:
                if video_file:
                    print("[INFO] Person found in the video file")
                    print("[INFO] Process took", process_elapsed_time, "to complete")
                    result_output_0= "Person FOUND!\t Elapsed Time "+ str(process_elapsed_time)[0:10]  +"\n\n"      # to update the results section
                    result_output_1=""
                    result_output_2=""
                    result_output_3=""
                    find=1      #to serialize results

                    # initializing to use at out side the loop
                    start_time, end_time= "", ""

                    # looping results list which returned from face_compare
                    total_results= 0
                    for frames in tracked_list:
                        current_index= tracked_list.index(frames)
                        if current_index % 2 ==0:
                            last_frame= tracked_list[current_index+1]
                            # for HH:MM:SS time format
                            if not video_file:
                                fps=30
                            # start_time = get_time_format((frames/fps), True)
                            # end_time= get_time_format((last_frame/fps), False)

                            start_time_seconds = int(frames / fps)
                            start_time_mins = int(start_time_seconds / 60)
                            start_time_seconds = int(start_time_seconds % 60)
                            start_time_hour = int(start_time_mins / 60)
                            start_time_mins = int(start_time_mins % 60)

                            start_time_string = str(start_time_hour) + ":" + str(start_time_mins) + ":" + str(start_time_seconds)

                            end_time_seconds = int(last_frame / fps)
                            end_time_mins = int(end_time_seconds / 60)
                            end_time_seconds = int(end_time_seconds % 60)
                            end_time_hour = int(end_time_mins / 60)
                            end_time_mins = int(end_time_mins % 60)

                            end_time_string = str(end_time_hour) + ":" + str(end_time_mins) + ":" + str(end_time_seconds)

                            if total_results >= 15:
                                result_output_2= "\nOnly showing first 15 results; All results are stored\nin Final_Results_Invidet.txt"
                                result_output_3 = result_output_3 + str(find) + ". " + person_name + " was found approximately during \n    " + start_time_string + " to " + end_time_string + ".\n"
                                print("\n[RESULTS]", person_name, "was found:")
                                print("[RESULTS] in frames, from frame number ", frames, " to ", last_frame)
                                print("[RESULTS] That is approximately Face Matched during time \n[RESULTS] ", start_time_string,
                                      "sec to ", end_time_string)
                                find += 1
                            else:
                                total_results += 1
                                result_output_1 = result_output_1 + str(find) + ". " +person_name+ " was found approximately during \n    " + start_time_string + " to " + end_time_string + ".\n"
                                print("\n[RESULTS]", person_name, "was found:")
                                print("[RESULTS] in frames, from frame number ", frames, " to ", last_frame)
                                print("[RESULTS] That is approximately Face Matched during time \n[RESULTS] ", start_time_string, "sec to ", end_time_string)
                                find+=1
                    find+= 1

                    # to handle remaining last time
                    if len(tracked_list) % 2 != 0:
                        if len(tracked_list)==1:
                            if str(tracked_list[0]) =="ERROR":
                                print("[ERROR] Fatal exception raised!\n[ERROR] Video cant be loaded")
                                window["-RES-"].update("Exception RAISED, Video Can't Load!\nCheck Video Path again")
                                break

                        frames = tracked_list[len(tracked_list) - 2]
                        last_frame = tracked_list[len(tracked_list) - 1]

                        # start_time = get_time_format((frames / fps), True)
                        # end_time = get_time_format((last_frame / fps), False)
                        start_time_seconds = int(frames / fps)
                        start_time_mins = int(start_time_seconds / 60)
                        start_time_seconds = int(start_time_seconds % 60)
                        start_time_hour = int(start_time_mins / 60)
                        start_time_mins = int(start_time_mins % 60)

                        start_time_string = str(start_time_hour) + ":" + str(start_time_mins) + ":" + str(
                            start_time_seconds)

                        end_time_seconds = int(last_frame / fps)
                        end_time_mins = int(end_time_seconds / 60)
                        end_time_seconds = int(end_time_seconds % 60)
                        end_time_hour = int(end_time_mins / 60)
                        end_time_mins = int(end_time_mins % 60)

                        end_time_string = str(end_time_hour) + ":" + str(end_time_mins) + ":" + str(end_time_seconds)

                        result_output_1 = result_output_1 + str(find) + ". " + person_name + " was found approximately during \n    " + start_time_string + " to " + end_time_string + ".\n"
                        print("\n[RESULTS]", person_name, "was found:")
                        print("[RESULTS] in frames, from frame number ", frames, " to ", last_frame)
                        print("[RESULTS] That is approximately Face Matched during time \n[RESULTS]", start_time_string, "sec to ", end_time_string)
                    window.refresh()
                    window["-RES-"].update(result_output_0+result_output_1+result_output_2)
                    result_text_file= open("Final_Results_Invidet.txt", "w")
                    result_text_file.truncate(0)
                    result_text_file.write(result_output_0+result_output_1+result_output_3)
                    result_text_file.close()

                else:       # if not a video file, means cam results
                    print("[INFO] Person found in the video file")
                    print("[INFO] Process took", process_elapsed_time, "to complete")
                    result_output_0 = "Person FOUND!\t Elapsed Time " + str(process_elapsed_time)[
                                                                        0:10] + "\n\n"  # to update the results section
                    result_output_1 = ""
                    result_output_2 = ""
                    result_output_3 = ""
                    # find = 1  # to serialize results

                    # initializing to use at out side the loop
                    start_time, end_time = "", ""

                    # looping results list which returned from face_compare
                    total_results = 0
                    for results in tracked_list:
                        # total_results += 1
                        if total_results >= 30:
                            result_output_2 = "\nOnly showing first 15 results; All results are stored\nin Final_Results_Invidet.txt"
                            result_output_3 = result_output_3+ str(results)
                            print("\n[RESULTS]", person_name, "was found:")
                            print("[RESULTS]", result_output_1, result_output_3)
                            # find += 1
                        else:
                            total_results += 1
                            result_output_1 = result_output_1 + str(results)  # to carry all results at once
                            # find += 1
                    # find += 1


                    window.refresh()
                    window["-RES-"].update(result_output_0 + result_output_1 + result_output_2)
                    result_text_file = open("Final_Results_Invidet.txt", "w")
                    result_text_file.truncate(0)
                    result_text_file.write(result_output_0 + result_output_1 + result_output_3)
                    result_text_file.close()

            else:
                result_output= person_name+ " was not Found!\tElapsed Time "+str(process_elapsed_time)[0:10]     # to update the results section
                print("[RESULTS] ", person_name, " was not found in the video file")
                window["-RES-"].update(result_output)
    # window.refresh()


window.close()