from operator import truediv
from typing import Set
import matlab
import matlab.engine
import threading
import time
import queue
import matlab_worker

"""
Class For Handling matlab calls
"""
class matlab_executioner:
    def __init__(self, retValQueue):
        self.matlabEngine = matlab.engine.start_matlab()
        self.matlabEngine.cd("..\matlabScripts")
        self.requests = queue.Queue(maxsize=10)
        self.finished = queue.Queue()
        self.retValQueue = retValQueue
        self.exit = threading.Event()
        self.workers = set()
        self.loopSleepTime = 0.3
        self.thread = threading.Thread(target=self.startMatlabServer, name="MatlabExecutionThread")
        self.thread.start()
    
    def __del__(self):
        self.exit.set()
        self.thread.join()
        for worker in self.workers:
            del worker

    def startMatlabServer(self):
        print("started matlab thread")
        while True:
            if self.exit.is_set():
                return
            try:
                request = self.requests.get_nowait()
                self.workers.add(matlab_worker.matlabWorker(self.matlabEngine, request))
            except queue.Empty:
                pass
            try:
                finishedWorker = self.finished.get_nowait()
                self.workers.remove(finishedWorker)
                finishedWorker.thread.join()
            except queue.Empty:
                pass

            time.sleep(self.loopSleepTime)

    def callTest(self, worker, request):
        a = request.args[0]
        b = request.args[1]
        retVal = worker.matlabEngine.test(a, b)
        if worker.exit.is_set():
            return
        self.retValQueue.put((request,retVal))
        finished = (worker)
        while True:
            try:
                self.finished.put(finished, block=True, timeout=1)
                return
            except queue.Full:
                if worker.exit.is_set():
                    return
                time.sleep(worker.loopSleepTime)

    def callFourier(self, worker, request):
        func = "@(t)" + request.args #+ "\""
        print(func)
        retVal = worker.matlabEngine.fourierTransform_base(func, nargout=0)
        if worker.exit.is_set():
            return
        self.retValQueue.put((request,retVal))
        finished = (worker)
        while True:
            try:
                self.finished.put(finished, block=True, timeout=1)
                return
            except queue.Full:
                if worker.exit.is_set():
                    return
                time.sleep(worker.loopSleepTime)

    def callJulia(self, worker, request):
        retVal = worker.matlabEngine.julia(request.args[0], request.args[1], request.args[2], request.args[3], nargout=0)
        if worker.exit.is_set():
            return
        self.retValQueue.put((request,retVal))
        finished = (worker)
        while True:
            try:
                self.finished.put(finished, block=True, timeout=1)
                return
            except queue.Full:
                if worker.exit.is_set():
                    return
                time.sleep(worker.loopSleepTime)
