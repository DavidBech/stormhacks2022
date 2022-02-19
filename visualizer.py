import figure_handle
import matlab_execution
import time
import queue
import matlab_request

"""
Top Level Module 
"""
if __name__ == "__main__":
    requestRetVals = queue.Queue()
    matlab_e = matlab_execution.matlab_executioner(requestRetVals)
    try:
        while True:
            try:
                val = requestRetVals.get_nowait()
                print("got item")
                print(f"Return Value: {val}")
            except queue.Empty:
                pass

            #print("Press Enter to create blank figure")
            #input()
            #request = matlab_request.request(matlab_e.createBlankFigure, None)
            #matlab_e.requests.put(request)
            print("before f transform")
            input()
            func = "cos(2*pi*2*t)"
            request = matlab_request.request(matlab_e.callFourier, (func))
            matlab_e.requests.put(request)
            print("after f transform")
            input()
            time.sleep(0.2)

    except KeyboardInterrupt:
        matlab_e.__del__()

    print("Exiting")
