import json
import smtplib
import ssl
import random

import PySimpleGUI as sg

# getting screen size
from screeninfo import get_monitors
from sys import exit




width= get_monitors()[0].width
height= get_monitors()[0].height
screensize=(int(width), int(height))



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
popups_font= "Akira 14"
h1= "Akira 30"
h2= "Akira 25"
h3= "Akira 10"
h33= "Akira 15"
# theme
sg.theme('dark grey 5')





available_product_keys= ["1FARZAN9", "2FAHAD99", "3FAROOQ9"]








# func

def info_encoder(pss):
    evalue = []
    for char in pss:
        evalue.append(ord(char))
    return evalue


def info_decoder(evalue):
    pss = ''
    for val in evalue:
        pss = pss + chr(val)
    return str(pss)



def send_otp(otp, email):
    try:
        port = 465
        sender_email = 'email@gmail.com'
        sender_email_pass = 'pass'
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
            server.login(sender_email, sender_email_pass)
            message = ('Your OTP is {}').format(otp)
            server.sendmail(sender_email, email, message)
        return
    except Exception as err:
        sg.Popup(err)
        return




# login window
def launch_login_window():
    # layout =
    layout=[
         [sg.Text('Login', font=login_had1, pad=((5,5),(200,20)))],
         [sg.Text('User Name: ', font=login_had3, pad=login_pad, size=(16, 1)), sg.In(font=login_had3, size=(16,1), key="-LGUSER-")],
         [sg.Text('Password: ', font=login_had3, size=(16, 1), pad=login_pad), sg.In(password_char="*", size= (16,1), font=login_had3, key="-LGPASS-")],
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
              [sg.Input(size=(35,1),key='-PRDCT-', font=login_had3, pad=login_pad, enable_events=True)],
              [sg.Button('Verify', pad=((5, 20), 10), font=login_had4, key="-VERIFY-", disabled= True)],
              [sg.T("Email", font=login_had3, size=(18, 1)),sg.Input(size=(16, 1), key='-EMAIL-', font=login_had3, pad=login_pad, disabled= True)],
              [sg.T("User Name", font=login_had3, size=(18,1)), sg.Input(size=(16,1),key='-SETUSERNAME-', font=login_had3, pad=login_pad, disabled= True)],
              [sg.T("Password", font=login_had3, size=(18,1)), sg.Input(size=(16,1),key='-SETPASS-', font=login_had3, pad=login_pad, password_char="*", disabled= True)],
			  [sg.T("Re-Enter Password", font=login_had3, size=(18, 1)), sg.Input(size=(16, 1), key='-SETPASS1-', font=login_had3, pad=login_pad, password_char="*", disabled= True)],
			  [sg.Button('Register', pad=((5,20),10), font=login_had4, key="-REGOK-", disabled= True)],
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
        # reg_email = values["-EMAIL-"]
        login_user_name = values["-LGUSER-"]
        login_password = values["-LGPASS-"]
        # reg_repassword = values["-SETPASS1-"]

        # check on all required fields must be filled
        if not login_user_name or not login_password:
            sg.popup_error("Missing Fields!", font= popups_font)
            continue

        # check on usernames and passwords must not contain spaces
        if (" " in login_user_name):
            sg.popup_error("User Name can't contain spaces!", font= popups_font)
            continue
        if (" " in login_password):
            sg.popup_error("Password can't contain spaces!", font= popups_font)
            continue

        # check on password length (pass: 8-15)
        if len(login_user_name) < 5 or len(login_user_name) > 10:
            sg.popup_error("Password must be 5 to 10 characters long", font= popups_font)
            continue

        # check on password length (pass: 8-15)
        if len(login_password) < 8 or len(login_password) > 15:
            sg.popup_error("Password must be 8 to 15 characters long", font= popups_font)
            continue

        # some sort of information encryption (manipulation with the asci values)
        # encrypted_reg_email = info_encoder(reg_email)
        # encrypted_reg_user_name = info_encoder(reg_user_name)
        # encrypted_reg_password = info_encoder(reg_password)

        with open('invidet_data.py', 'r') as read_data:
            user_data_dictionary = json.load(read_data)
        decrypted_username = info_decoder(user_data_dictionary["username"])
        decrypted_password = info_decoder(user_data_dictionary["password"])

        if login_user_name != decrypted_username:
            sg.popup("User is not registered!", font= popups_font)
            continue
        if login_password != decrypted_password:
            sg.popup("Wrong Password!", font= popups_font)
            continue




        # # finally writing information in file to use later
        # user_data_dictionary = {"email": encrypted_reg_email, "username": encrypted_reg_user_name,
        #                         "password": encrypted_reg_password}
        # dic.update({'sqs': False})
        with open('invidet_data.py', 'w') as write:
            json.dump(user_data_dictionary, write)

        sg.popup("Successfully Logged-in!")



        main_window = launch_main_window()
        login_window.close()
        login_window = None
        register_window = None

    # handling popup event if clicked forget password
    if event == "-FORGET-":

        entered_email = sg.popup_get_text('Enter your email address', 'Forget Password', size=(20,3), font=popups_font)
        with open("invidet_data.py", "r") as read_data:
            user_data_dictionary= json.load(read_data)
        decrypted_email = info_decoder(user_data_dictionary["email"])

        entered_email= entered_email.lower()
        if entered_email != decrypted_email:
            sg.popup_error("Your entered email is not in registered record")
            continue


        generated_otp=random.randint(111111, 999999)
        print("otp: ", generated_otp)
        # send_otp(generated_otp, entered_email)

        entered_otp = sg.popup_get_text('Enter OTP', 'Forget Password', size=(20,3), font=popups_font)


        if str(generated_otp) != str(entered_otp):
            sg.popup_error("OTP is wrong! exiting")
            continue

        sg.popup('Remember Credentials!', 'User Name: '+ str(info_decoder(user_data_dictionary["username"])), "Password: " + str(info_decoder(user_data_dictionary["password"])) , font= popups_font)




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
        reg_email= values["-EMAIL-"]
        reg_user_name= values["-SETUSERNAME-"]
        reg_password= values["-SETPASS-"]
        reg_repassword= values["-SETPASS1-"]

        # check on all required fields must be filled
        if not reg_email or not reg_user_name or not reg_password or not reg_repassword:
            sg.popup_error("Missing Fields!", font= popups_font)
            continue

        # check on email and usernames and passwords must not contain spaces
        if (" " in reg_email):
            sg.popup_error("Email can't contain spaces!", font= popups_font)
            continue
        if (" " in reg_user_name):
            sg.popup_error("User Name can't contain spaces!", font= popups_font)
            continue
        if (" " in reg_password or " " in reg_repassword):
            sg.popup_error("Password can't contain spaces!", font= popups_font)
            continue

        # check on email validity
        if not reg_email.endswith("@gmail.com"):
            sg.popup_error("Email is not valid", font= popups_font)
            continue

        # check on username length (validity 5-10)
        if len(reg_user_name) < 5 or len(reg_user_name) > 10:
            sg.popup_error("user name must be 5 to 10 characters long", font= popups_font)
            continue

        # check on password length (validity 8-15)
        if len(reg_password) < 8 or len(reg_password) >15 or len(reg_repassword) < 8 or len(reg_repassword) > 15:
            sg.popup_error("Password must be 8 to 15 characters long", font= popups_font)
            continue

        # check on password match
        if not reg_password == reg_repassword:
            sg.popup_error("Password doesn't match!", font= popups_font)
            continue

        # some sort of information encryption (manipulation with the asci values)
        encrypted_reg_email= info_encoder(reg_email)
        encrypted_reg_user_name= info_encoder(reg_user_name)
        encrypted_reg_password= info_encoder(reg_password)

        # finally writing information in file to use later
        user_data_dictionary = {"email": encrypted_reg_email, "username": encrypted_reg_user_name, "password": encrypted_reg_password}
        # dic.update({'sqs': False})
        with open('invidet_data.py', 'w') as write:
            json.dump(user_data_dictionary, write)

        sg.popup("Successfully Registered!", font= popups_font)


        # making these fields disabled again so not everyone can register himself
        window["-REGOK-"].update(disabled=True)
        window["-EMAIL-"].update(disabled=True)
        window["-SETUSERNAME-"].update(disabled=True)
        window["-SETPASS-"].update(disabled=True)
        window["-SETPASS1-"].update(disabled=True)

        # print("email: ", encrypted_reg_email)
        # print("user name: ", encrypted_reg_user_name)
        # print("password: ", encrypted_reg_password)

        # window.refresh()
        # if (" " in reg_email):
        #     print("Email cant have spaces")


        # print("Email cant have spaces")
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

    if event == "-VERIFY-":
        # obtaining product key from user
        product_key= values["-PRDCT-"]

        # matching the key if available
        if product_key in available_product_keys:
            window["-REGOK-"].update(disabled= False)
            window["-EMAIL-"].update(disabled= False)
            window["-SETUSERNAME-"].update(disabled= False)
            window["-SETPASS-"].update(disabled= False)
            window["-SETPASS1-"].update(disabled= False)
            sg.popup("Successfully Verified!\nNow you can create account", font= popups_font)

        else:
            sg.popup_error("Product key is not valid", font= popups_font)
            continue

    if event == "-PRDCT-":
        product_key = values["-PRDCT-"]
        if len(product_key) == 8:
            window["-VERIFY-"].update(disabled=False)
        else:
            window["-VERIFY-"].update(disabled=True)

window.close()