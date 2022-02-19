import matlab
import matlab.engine
import io
"""
Class For Handling matlab calls
"""
class matlab_executioner:
    def __init__(self):
        self.matlabEngine = matlab.engine.start_matlab()
        self.matlabEngine.cd("matlabScripts")
        self.matlabOut = io.StringIO()
        self.matlabErr = io.StringIO()

    def getMLabStdout(self) -> str:
        return self.matlabOut.getvalue()

    def getMLabStderr(self) -> str:
        return self.matlabErr.getvalue()

    def callTest(self):
        print(self.matlabEngine.test(2,3))
    
    def callFourier(self):
        print(self.matlabEngine.fourierTransform_base(" "))