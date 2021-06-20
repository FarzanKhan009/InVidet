import PySimpleGUI as sg

from sys import exit

from screeninfo import get_monitors
# for m in get_monitors():
#     print(str(m))

width= get_monitors()[0].width
height= get_monitors()[0].height
screensize=(int(width), int(height))
print(screensize, type(screensize))
# print("screen", get_monitors(), type(get_monitors()), get_monitors()[0].height, type(get_monitors()[0]))



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
              [sg.Button('OK', pad=login_pad, font=login_had4), sg.Button('Exit', font=login_had4, pad=login_pad)]]
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
         sg.Radio('0.6', "RADIO1", size=(4, 1), pad=setting_pad, font=h3, key="-TH3-")],

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
    if event == sg.WIN_CLOSED or event == '-LOGEXIT-':

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

    if event == 'Popup':
        sg.popup('This is a BLOCKING popup','all windows remain inactive while popup active')
    if event == '-REGBTN-' and not register_window and not main_window:
        register_window = launch_register_window()
        login_window = None
        main_window = None

    if event == "-LOGINBTN-" and not register_window and not main_window:
        register_window = None
        main_window = launch_main_window()
        login_window.close()
    if event == '-IN-':

        window['-OUTPUT-'].update(f'You enetered {values["-IN-"]}')
    if event == 'Erase':

        window['-OUTPUT-'].update('')

        window['-IN-'].update('')


window.close()