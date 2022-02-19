import matlab
import matlab.engine

class matlab_executioner:
    def __init__(self):
        self.matlabEngine = matlab.engine.start_matlab()
        pass
