import matlab.engine
import threading

"""
Matlab Worker
"""

class matlabWorker:
    staticCounter = 1
    def __init__(self, engine, command, *args):
        self.id = matlabWorker.staticCounter
        self.name = f"Worker{self.id}"
        matlabWorker.staticCounter += 1
        self.matlabEngine = engine
        self.exit = threading.Event()
        self.thread = threading.Thread(target=command, name=self.name, args=(self, args))
        self.thread.start()

    def __del__(self):
        self.exit.set()
        self.thread.join()

    def __str__(self)->str:
        return f"Worker {self.id}, Running:{self.thread.is_alive()}"

    def __repr__(self)->str:
        return self.__str__()

