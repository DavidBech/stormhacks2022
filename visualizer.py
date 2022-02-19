import figure_handle
import matlab_execution
import time

"""
Top Level Module 
"""
if __name__ == "__main__":
    matlab_e = matlab_execution.matlab_executioner()
    try:
        while True:
            print("Enter Value for a")
            a = int(input())
            print("Enter Value for b")
            b = int(input())
            request = (matlab_e.callTest, (a,b))
            matlab_e.requests.put(request)
            time.sleep(0.2)
    except KeyboardInterrupt:
        matlab_e.__del__()

    print("Exiting")
