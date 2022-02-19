
class request:
    def __init__(self, matlabFunc, args):
        self.command = matlabFunc
        self.args = args

    def __str__(self)->str:
        return f"Reqest:{self.command}({self.args})"

    def __repr__(self)->str:
        return self.__str__()
