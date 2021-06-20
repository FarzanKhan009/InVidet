import PySimpleGUI as sg

from sys import exit

import times
from cv2 import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip
from screeninfo import get_monitors
# for m in get_monitors():
#     print(str(m))
from face_compare import compare_faces

width= get_monitors()[0].width
height= get_monitors()[0].height
screensize=(int(width), int(height))
print(screensize, type(screensize))
# print("screen", get_monitors(), type(get_monitors()), get_monitors()[0].height, type(get_monitors()[0]))




threshold, v_fps, fps, duration =0.5,1,0,0      # defaults
v_out, v_show, video_file= False, False, True
picture_input, video_input, person_name ="", "", "Anonymous"
aprx_ratio= 0.75
time = (duration * aprx_ratio) + 10
first = 0       #to check first loop in GUI, for fetching results




# to use in padding tupple
general_size= (int(width/90), 1)
output_height=int(height/18)
output_width=int(width/3)

inputs_pad_standard= ((5,5),2)
setting_pad= ((5,5), (1,1))
login_pad= (5,10)
login_had1= "Akira 30"
login_had2= "Akira 25"
login_had3= "Akira 20"
login_had4= "Akira 15"
h1= "Akira 30"
h2= "Akira 25"
h3= "Akira 10"
h33= "Akira 15"
# theme
sg.theme('BluePurple')






# take seonds in seconds and return a string with format
def get_time_format(seconds, start):

    minutes,hours=0,0
    time_string = ""
    if seconds >= 60:    # check if it exceed 1 minut
        minutes = int(seconds / 60)
        seconds = int(seconds % 60)
        if minutes >= 60:    # check if it exceed 1 hour
            hours = int(minutes / 60)
            minutes = int(minutes % 60)
            if len(str(seconds))<2:     # beautifying by adding 0 in between 10:44:05
                seconds = "0" + str(seconds)
            if len(str(minutes))<2:     # 10:02:45
                minutes = "0" + str(minutes)
            if len(str(hours))<2:       # 07:55:12
                minutes = "0" + str(minutes)
            if start:
                time_string = str(hours) + ":" + str(minutes) + ":" + str(seconds)
            else:
                time_string = str(hours) + ":" + str(minutes) + ":" + str(seconds) + " (Hours:Minutes:Seconds)"
        else:
            if len(str(seconds))<2:     # beautifying
                seconds = "0" + str(seconds)
            if len(str(minutes))<2:
                minutes = "0" + str(minutes)
            if start:
                time_string = str(minutes) + ":" + str(seconds)
            else:
                time_string = str(minutes) + ":" + str(seconds) + " (Minutes:Seconds)"
    else:
        # seconds = int(seconds)
        if seconds <10:
            seconds = "0" + str(seconds)[0:3]
        if start:
            time_string = str(seconds)[0:4]
        else:
            time_string = str(seconds)[0:4] + " (Seconds)"
    return time_string







def launch_login_window():
    # layout =
    layout=[
         [sg.Text('Login', font=login_had1, pad=((5,5),(200,20)))],
         [sg.Text('User Name: ', font=login_had3, pad=login_pad, size=(16, 1)), sg.In(font=login_had3, size=(16,1))],
         [sg.Text('Password: ', font=login_had3, size=(16, 1), pad=login_pad), sg.In(password_char="*", size= (16,1), font=login_had3)],
         [sg.Button('Login', key="-LOGINBTN-", pad=login_pad)],
         [sg.T("\n\n\n\nNot Registered?", font=h2, pad=login_pad)],
         [sg.Button("Register Now", key='-REGBTN-', font=h3, pad=login_pad), sg.Button('Exit', key="-LOGEXIT-", font=h3)]
    ]
    in_col=[[sg.Column(layout, element_justification="l", vertical_alignment="center")]]
    return sg.Window('Login Window', in_col, location=(0,0), element_justification="c", size=screensize, finalize=True)

def launch_register_window():
    layout = [[sg.Text('Registration', font=login_had1, pad=((5,5), (200,20)))],
              [sg.T("\nEnter 8 digit product key", font=login_had4, pad=login_pad)],
              [sg.Input(size=(32,1),key='-PRDCT-', font=login_had3, pad=login_pad)],
              [sg.Button('OK', pad=((5,20),10), font=login_had4, key="-REGOK-")],
              [sg.Button('Login Screen', key="-BKLOGIN-", font=h3, pad=login_pad), sg.Button('Exit', key="-REGEXIT-", font=h3, pad=login_pad)]]
    in_col=[[sg.Col(layout, element_justification="l", vertical_alignment="c")]]
    return sg.Window('Second Window', in_col,location=(0,0), element_justification="c", size=screensize, finalize=True)

def launch_main_window():

    title_layout = [[
        sg.Text('InVid Detector', justification='center', font=h1)
    ]]

    left_inputs_setting_col = [
        # picture_video_selection_layout
        [sg.T("Inputs", font=h2, pad=inputs_pad_standard, size= general_size)],
        [sg.T('Select Picture', pad=inputs_pad_standard, key="-SPIC-", size=(20, 1), font=h33),
         sg.In(key='-PICIN-', pad=inputs_pad_standard, visible=False),
         sg.FilesBrowse(target='-PICIN-', pad=inputs_pad_standard)],
        [sg.T('Select Video', pad=inputs_pad_standard, key="-SVID-", size=(20, 1), font=h33),
         sg.In(key='-VIDIN-', pad=inputs_pad_standard, visible=False),
         sg.FilesBrowse(target='-VIDIN-', pad=((5, 5), (2, 15)), disabled=False, key="-VBRS-")],

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
        [sg.Text("Person name if known? (optional)", pad=setting_pad, font=h33)],
        [sg.Input(key="-PRNAME-", size=(16, 1), pad=setting_pad, font=h3)],

        # threshold_layout
        [sg.T("Select a threshold value", pad=setting_pad, font=h33)],
        [sg.Radio('0.4', "RADIO1", size=(4, 1), pad=setting_pad, font=h3, key="-TH1-"),
         sg.Radio('0.5', "RADIO1", default=True, size=(4, 1), pad=setting_pad, font=h3, key="-TH2-"),
         sg.Radio('0.6', "RADIO1", size=(4, 1), pad=setting_pad, font=h3, key="-TH3-"),
         sg.Radio('0.7', "RADIO1", size=(4, 1), pad=setting_pad, font=h3, key="-TH4-")],

        # verifying_layout
        [sg.T("Select Verifying fps", pad=setting_pad, font=h33)],
        [sg.Radio("V1FPS", "RADIO2", default=True, font=h3, pad=setting_pad, size=(6, 1), key="-FPS1-"),
         sg.Radio("V2FPS", "RADIO2", font=h3, pad=setting_pad, size=(6, 1), key="-FPS2-")],
        [sg.Radio("V3FPS", "RADIO2", font=h3, pad=setting_pad, size=(6, 1), key="-FPS3-"),
         sg.Radio("V4FPS", "RADIO2", font=h3, pad=setting_pad, size=(6, 1), key="-FPS4-")],

        # write_video_layout
        [sg.T("Output a video file?", pad=setting_pad, font=h33)],
        [sg.Radio("No", "RADIO3", default=True, font=h3, pad=setting_pad, size=(6, 1), key="-VOUT1-"),
         sg.Radio("Yes", "RADIO3", font=h3, pad=setting_pad, size=(6, 1), key="-VOUT2-")],
        [sg.T("Display video??", pad=setting_pad, font=h33)],
        [sg.Radio("No", "RADIO4", default=True, font=h3, pad=setting_pad, size=(6, 1), key="-VSHOW1-"),
         sg.Radio("Yes", "RADIO4", font=h3, pad=setting_pad, size=(6, 1), key="-VSHOW2-")],
        [sg.B("SET", key='-SET-', pad=setting_pad)],

        # horisotal
        [sg.HSeparator()],
        # set_choice_layout
        [sg.T("Set Threshold\t: 0.5   (default)", pad=setting_pad, font=h3, key="-DFLT1-", size=(30, 1))],
        [sg.T("Verify Frame Rate\t: 1FPS  (default)", pad=setting_pad, font=h3, key="-DFLT2-", size=(30, 1))],
        [sg.T("Write Video\t: NO    (default)", pad=setting_pad, font=h3, key="-DFLT3-", size=(30, 1))],
        [sg.T("Display Video\t: NO    (default)", pad=setting_pad, font=h3, key="-DFLT4-", size=(30, 1))],
        # aprx time to process
        [sg.T("Estimated time to process: ", pad=setting_pad, font=h3, key="-APRX-", size=(28, 1))],

        # buttons
        [sg.B("Start Processing", key='-START-', pad=setting_pad, font=h3),
         sg.B("Exit", key='-MAINEXIT-', pad=setting_pad, font=h3),
         sg.T("Error! Inputs Can't Load", font=h3, visible=False, key="-ERR-", text_color="red")]
    ]

    right_col = [
        [sg.T("Output Logs", font=h2, pad=inputs_pad_standard)],
        [sg.Output(size=(output_width,output_height))]
    ]
    mid_column = [
        [sg.T("Final Results", font=h2, pad=inputs_pad_standard)],
        [sg.T("Time Elapsed: ", visible=False, font=h3, key="-TIME-")],
        [sg.T("Results", key="-RES-", size=(output_width,output_height), font=h3)],
        # [sg.HSeparator()]
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
    print("[INFO] Launching GUI")
    return sg.Window('InVid Detector', layout, location=(0,0), size=screensize, finalize=True)

login_window, register_window, main_window = launch_login_window(), None, None        # start off with 1 window open


while True:             # Event Loop

    window, event, values = sg.read_all_windows()
    print("window object: ", window)
    if event == sg.WIN_CLOSED or event == '-LOGEXIT-' or event == "-REGEXIT-" or event == "-MAINEXIT-":

        if window == register_window:       # if closing win 2, mark as closed
            window.close()
            register_window = None
            # exit()
            # window.close()
        if window == main_window:
            window.close()
            main_window = None
            # exit()

        if window == login_window:     # if closing win 1, exit program
            login_window = None
            window.close()
            # exit()
        exit()

    # taking control back to login window
    if event == "-REGOK-":
        login_window = launch_login_window()
        register_window.close()
        register_window = None
        main_window = None


    # taking control to Registration screen
    if event == '-REGBTN-' and not register_window and not main_window:
        register_window = launch_register_window()
        login_window.close()
        login_window = None
        main_window = None

    # taking back to login screen
    if event == "-BKLOGIN-" and not login_window and not main_window:
        login_window = launch_login_window()
        register_window.close()
        register_window = None
        main_window = None

    if event == "-LOGINBTN-" and not register_window and not main_window:
        main_window = launch_main_window()
        login_window.close()
        login_window = None
        register_window = None



    # handling video stream choice
    if event == "-VIN1-":
        video_file=False
        print("[INFO] Video source changed to Cam Stream")
        window["-VBRS-"].update(disabled=True)
    if event == "-VIN2-":
        video_file=True
        print("[INFO] Video source changed to video file on disc")
        window["-VBRS-"].update(disabled=False)

    if event == "-SET-":
        # setting threshold
        # print("[INFO] Setting choices")
        if len(window["-PRNAME-"].get()):
            person_name= window["-PRNAME-"].get()
        if window["-TH1-"].get():
            window["-DFLT1-"].update("Set Threshold\t: 0.4")
            threshold= 0.4
        if window["-TH2-"].get():
            window["-DFLT1-"].update("Set Threshold\t: 0.5   (default)")
            threshold= 0.5
        if window["-TH3-"].get():
            window["-DFLT1-"].update("Set Threshold\t: 0.6")
            threshold= 0.6
        if window["-TH4-"].get():
            window["-DFLT1-"].update("Set Threshold\t: 0.7")
            threshold= 0.7
        # setting fps
        if window["-FPS1-"].get():
            window["-DFLT2-"].update("Verify Frame Rate\t: 1FPS  (default)")
            aprx_ratio= 0.75
            time = (duration * aprx_ratio) + 10
            window["-APRX-"].update("Estimated time to process: %s" % time)
            v_fps= 1
        if window["-FPS2-"].get():
            window["-DFLT2-"].update("Verify Frame Rate\t: 2FPS")
            aprx_ratio= 1.5
            time = (duration * aprx_ratio) + 10
            window["-APRX-"].update("Estimated time to process: %s" % time)
            v_fps= 2
        if window["-FPS3-"].get():
            window["-DFLT2-"].update("Verify Frame Rate\t: 3FPS")
            aprx_ratio= 2.25
            time = (duration * aprx_ratio) + 10
            window["-APRX-"].update("Estimated time to process: %s" % time)
            v_fps= 3
        if window["-FPS4-"].get():
            window["-DFLT2-"].update("Verify Frame Rate\t: 4FPS")
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

        if window["-VSHOW1-"].get():
            window["-DFLT4-"].update("Show Video\t: NO    (default)")
            v_show= False
        if window["-VSHOW2-"].get():
            window["-DFLT4-"].update("Show Video\t: YES")
            v_show= True

        print("\n[INFO] User choices")
        print("[INFO] Thresholds: ", threshold)
        print("[INFO] FPS: ", v_fps)
        print("[INFO] Video OUT: ", v_out)
        print("[INFO] Video SHOW: ", v_show)
        print("[INFO] Estimated time to process: ", (duration* aprx_ratio)+10)    # 0.75 is ratio on my pc for v1FPS +10 tensor flow loading delay


    if event == '-LOAD-':
        picture_input=values["-PICIN-"]
        video_input= values["-VIDIN-"]
        window.refresh()
        if len(picture_input)>0:
            image_extension= picture_input.rsplit(".", 1)[1]
            # check on extension
            if image_extension not in ["tif", "tiff", "bmp", "jpg", "jpeg", "gif", "png", "esp"]:
                print("[ERROR] Image file extension is not known\n[ERROR] Check Image path, chose again with known image\n[ERROR] extensions instead of .%s" %image_extension)
                window["-SPIC-"].update("Picture Error")
                continue

            print("[INFO] Picture is loaded")
            window["-SPIC-"].update("Picture SELECTED")
            pic_url = picture_input.rsplit("/", 1)
            pic_url = "Picture name: %s" % pic_url[1]
            window["-PNAME-"].update(value=str(pic_url))
        else:
            print("[WARN] Picture is MISSING")
        window.refresh()
        if len(video_input)>0:

            video_extension= video_input.rsplit(".", 1)[1]
            # check on extension
            if video_extension not in ["mp4", "MP4", "MOV", "mov", "WMV", "wmv", "FLV", "flv" , "AVI", "avi", "AVCHD", "avchd", "WebM", "webm", "MKV", "mkv"]:
                print("[ERROR] Video file extension is not known\n[ERROR] Check Video path, chose again with known Video\n[ERROR] extensions instead of .%s" %video_extension)
                window["-SVID-"].update("Video Error")
                continue

            print("[INFO] Video is loaded")
            window["-SVID-"].update("Video SELECTED")
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
        else:
            print("[WARN] Video is MISSING")
        # window.refresh()

        if len(picture_input)>0 and len(video_input)>0:
            print("[INFO] Inputs are loaded successfully")
            window["-ERR-"].update(visible=False)
            window.refresh()

        # threshold= window["TH1"].get()
        # print(threshold, type(threshold))
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
            track_records= compare_faces(picture_input, video_input, fps, threshold, v_fps, person_name, v_out, v_show, video_file)
            # track_records= compare_faces(picture_input, video_input)
            process_elapsed_time = times.now() - process_start
            if len(track_records) >0:
                print("[INFO] Person found in the video file")
                print("[INFO] Process took", process_elapsed_time, "to complete")
                result_output_0= "Person FOUND!\t Elapsed Time "+ str(process_elapsed_time)[0:10]  +"\n\n"      # to update the results section
                result_output_1=""
                find=1      #to serialize results

                # initializing to use at out side the loop
                start_time, end_time= "", ""

                # looping results list which returned from face_compare
                for frames in track_records:
                    current_index= track_records.index(frames)
                    if current_index % 2 ==0:
                        last_frame= track_records[current_index+1]
                        # for HH:MM:SS time format
                        if not video_file:
                            fps=30
                        start_time = get_time_format((frames/fps), True)
                        end_time= get_time_format((last_frame/fps), False)


                        result_output_1 = result_output_1 + str(find) + ". " +person_name+ " was found approximately during \n    " + str(start_time) + " to " + str(end_time) + ".\n"
                        print("\n[RESULTS]", person_name, "was found:")
                        print("[RESULTS] in frames, from frame number ", frames, " to ", last_frame)
                        print("[RESULTS] That is approximately Face Matched during time \n[RESULTS] ", start_time, "sec to ", end_time)
                        find+=1
                find+= 1

                # to handle remaining last time
                if len(track_records) % 2 != 0:
                    if len(track_records)==1:
                        if str(track_records[0]) =="ERROR":
                            print("[ERROR] Fatal exception raised!\n[ERROR] Video cant be loaded")
                            window["-RES-"].update("Exception RAISED, Video Can't Load!\nCheck Video Path again")
                            break

                    frames = track_records[len(track_records) - 2]
                    last_frame = track_records[len(track_records) - 1]

                    start_time = get_time_format((frames / fps), True)
                    end_time = get_time_format((last_frame / fps), False)

                    result_output_1 = result_output_1 + str(find) + ". " + person_name + " was found approximately during \n    " + str(start_time) + " to " + str(end_time) + ".\n"
                    print("\n[RESULTS]", person_name, "was found:")
                    print("[RESULTS] in frames, from frame number ", frames, " to ", last_frame)
                    print("[RESULTS] That is approximately Face Matched during time \n[RESULTS]", start_time, "sec to ", end_time)
                window.refresh()
                window["-RES-"].update(result_output_0+result_output_1)
            else:
                result_output= person_name+ " was not Found!\tElapsed Time "+str(process_elapsed_time)[0:10]     # to update the results section
                print("[RESULTS] ", person_name, " was not found in the video file")
                window["-RES-"].update(result_output)


window.close()