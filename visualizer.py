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

            request = matlab_request.request(matlab_e.callJulia, (25, 1000, -0.8, 0.158))
            matlab_e.requests.put(request)
            print("after julia")
            input()
            time.sleep(0.2)

    except KeyboardInterrupt:
        matlab_e.__del__()

    print("Exiting")
