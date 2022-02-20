import PySimpleGUI as sg
import sys
sys.path.insert(1, '..')
import matlab_execution
import figure_handle
import matlab_request
import queue
import PIL.Image

#sg.preview_all_look_and_feel_themes()
sg.theme('BlueMono')   # Add a touch of color
# WHAT ARE YOU FEEEEEEELING?

# All the stuff inside your window.
layoutFourier = [
            [sg.Text('Enter value a'), sg.InputText()],
            [sg.Text('Enter value b'), sg.InputText()]
        ]

layoutJulia = [
            [sg.Text('Real c value'), sg.InputText()],
            [sg.Text('Complex c value'), sg.InputText()]
        ]

layout = [
            [sg.Image('juliaSet.png', key="-IMAGE-")],
            [
                sg.Column(layoutFourier, key="layoutFourier"), 
                sg.Column(layoutJulia, visible=False, key="layoutJulia")
            ],
            [sg.Button('Ok')],
            [sg.Button("Change Window")],
            [sg.Button('Cancel')]
        ]

currentLayout="layoutFourier"
# Create the Window
window = sg.Window("Visualizer", layout)

requestRetVals = queue.Queue()
matlab_e = matlab_execution.matlab_executioner(requestRetVals)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    
    # Switch mode between fourier and julia set
    if event == 'Change Window':
        window[f"{currentLayout}"].update(visible=False)
        currentLayout = "layoutFourier" if currentLayout == "layoutJulia" else "layoutJulia"
        window[f"{currentLayout}"].update(visible=True)
        window.refresh()

    # attempt to get any return value from pervious matlab calls
    try:
        val = requestRetVals.get_nowait()
        print(f"Return Value: {val}")
        if currentLayout == "layoutFourier":
            if "fourier" in val[1]:
                window["-IMAGE-"].update("..\matlabScripts\fourierMag.png")
        elif currentLayout == "layoutJulia":
            if "julia" in val[1]:
                window["-IMAGE-"].update("..\matlabScripts\juliaSet.png")
    except queue.Empty:
        pass
    
    #Pass in arguments to request portal
    if event == "Ok":
        if currentLayout == "layoutFourier":
            request = matlab_request.request(matlab_e.callFourier, (int(values[1]), int(values[2])))
        elif currentLayout == "layoutJulia":
            request = matlab_request.request(matlab_e.callJulia, (25, 1000, float(values[2]), float(values[3])))
            
        matlab_e.requests.put(request)
    
window.close()
matlab_e.__del__()