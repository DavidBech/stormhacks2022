from operator import truediv
from typing import Set
import matlab
import matlab.engine
import io
import threading
import time
import queue
import matlab_worker

"""
Class For Handling matlab calls
"""
class matlab_executioner:
    def __init__(self):
        self.matlabEngine = matlab.engine.start_matlab()
        self.matlabEngine.cd("matlabScripts")
        self.requests = queue.Queue(maxsize=10)
        self.finished = queue.Queue()
        self.exit = threading.Event()
        self.workers = set()
        self.thread = threading.Thread(target=self.startMatlabServer, name="MatlabExecutionThread")
        self.thread.start()
    
    def __del__(self):
        print("in matlab delete")
        self.exit.set()
        self.thread.join()
        print(f"ending workers {self.workers}")
        for worker in self.workers:
            del worker

    def startMatlabServer(self):
        print("started matlab thread")
        while True:
            if self.exit.is_set():
                print("Exiting Matlab Executioner")
                return
            try:
                request = self.requests.get_nowait()
                self.workers.add(matlab_worker.matlabWorker(self.matlabEngine, request[0], request[1]))
            except queue.Empty:
                pass
            try:
                finishedWorker = self.finished.get_nowait()
                self.workers.remove(finishedWorker)
                finishedWorker.thread.join()
            except queue.Empty:
                pass

            time.sleep(0.3)
            print("time")

    def callTest(self, worker, *args):
        retVal = worker.matlabEngine.test(2,3)
        if worker.exit.is_set():
            return
        print(retVal)
        finished = (worker)
        while True:
            try:
                self.finished.put(finished, block=True, timeout=1)
                return
            except queue.Full:
                if worker.exit.is_set():
                    return
                time.sleep(0.3)
    
    def callFourier(self, engine):
        print(engine.fourierTransform_base(" "))
