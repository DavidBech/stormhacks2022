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
                print(f"Return Value: {val}")
            except queue.Empty:
                pass

            print("Enter Value for a")
            a = int(input())
            print("Enter Value for b")
            b = int(input())
            request = matlab_request.request(matlab_e.callTest, (a,b))
            matlab_e.requests.put(request)
            time.sleep(0.2)
    except KeyboardInterrupt:
        matlab_e.__del__()

    print("Exiting")
