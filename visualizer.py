import figure_handle
import matlab_execution
"""
Top Level Module 
"""
if __name__ == "__main__":
    matlab_e = matlab_execution.matlab_executioner()
    open = True
    while open:
        input()
        matlab_e.callFourier()

    print("Exiting")
