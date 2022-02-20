import PySimpleGUI as sg
import sys
sys.path.insert(1, '..')
import matlab_execution
import figure_handle
import matlab_request
import queue
import PIL.Image
import math

#sg.preview_all_look_and_feel_themes()
sg.theme('BlueMono')   # Add a touch of color
# WHAT ARE WE FEEEEEEELING?

# All the stuff inside your window.
layoutFourier = [
            [sg.Text('Fast Fourier Transform')],
            [sg.Text('Enter function of t'), sg.InputText()]
        ]

layoutJulia = [
            [sg.Text('Julia Set: '), sg.Image('juliaSetFormula.png')],
            [sg.Text("Slide to select a value for 'a'"), sg.Slider(range=(0,6.2), default_value=3.14, resolution=.1, size=(40,15), orientation='horizontal', key='juliaInputCount')],
            #[sg.Slider(range=(0,6.2), default_value=3.14, resolution=.1, size=(40,15), orientation='horizontal')]
        ]

layout = [
            [sg.Image('juliaSet.png', key="-IMAGE-")],
            [
                sg.Column(layoutFourier, key="layoutFourier"), 
                sg.Column(layoutJulia, visible=False, key="layoutJulia")
            ],
            [sg.Button('Ok'), sg.Button("Change Window"), sg.Button('Cancel')]
        ]

currentLayout="layoutFourier"
# Create the Window
window = sg.Window("Visualizer", layout)

requestRetVals = queue.Queue()
matlab_e = matlab_execution.matlab_executioner(requestRetVals, window)
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
        # print(f"Return Value: {val}")
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
            request = matlab_request.request(matlab_e.callFourier, values[2])
        elif currentLayout == "layoutJulia":
            #real = cos(c) and complex = sin(c); multiply both real and complex values by 0.7885
            real = 0.7885*math.cos(float(values['juliaInputCount']))
            complex = 0.7885*math.sin(float(values['juliaInputCount']))
            request = matlab_request.request(matlab_e.callJulia, (25, 1000, real, complex))
            
        matlab_e.requests.put(request)
    
window.close()
matlab_e.__del__()