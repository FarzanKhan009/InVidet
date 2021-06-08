import PySimpleGUI as sg
# from window import *



sg.theme('BluePurple')
layout_column = [
        [sg.Text('InVid Detector',justification='center', font="Courier 20")],
        ]

# title_layout=[sg.Column([sg.T("InVid Detector", justification="center")], element_justification="center")]
# title_column=
input_layout= [[sg.T('Select Picture', pad=((20,10),30)), sg.In(key='pic_in', pad=((10,10),30)), sg.FilesBrowse(target='pic_in', pad=((10,50),30)), sg.T('Select Video', pad=((50,10),30)), sg.In(key='vid_in', pad=((10,10),30)), sg.FilesBrowse(target='vid_in', pad=((10,20),30))]]


layout = [
          [sg.Column(layout_column, element_justification='center', pad=(440,0))],
          input_layout,
          ]



window = sg.Window('InVid Detector', layout, size=(1200, 800), finalize= True)
while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    print(values["pic_in"])
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Show':
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].update(values['-IN-'])

window.close()