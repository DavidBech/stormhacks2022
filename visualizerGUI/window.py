import PySimpleGUI as sg
import sys
sys.path.insert(1, '..')
import matlab_execution
import figure_handle
import matlab_request
import queue

#sg.preview_all_look_and_feel_themes()
sg.theme('BlueMono')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Enter value a'), sg.InputText()],
            [sg.Text('Enter value b'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Window Title', layout)

requestRetVals = queue.Queue()
matlab_e = matlab_execution.matlab_executioner(requestRetVals)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    
    try:
        val = requestRetVals.get_nowait()
        print(f"Return Value: {val}")
    except queue.Empty:
        pass

    #Pass in arguments to request portal
    request = matlab_request.request(matlab_e.callTest, (int(values[0]), int(values[1])))
    matlab_e.requests.put(request)
    
window.close()
matlab_e.__del__()