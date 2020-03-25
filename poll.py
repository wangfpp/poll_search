## coding: utf-8

import threading
from server import Search
import queue

class Poll(object):
    def __init__(self, poll_num = 2):
        self.poll_num = poll_num
        self.threadingList = []
        self._queue = queue.Queue()
        self._stop = False
        self.runPoll()
    
    def runPoll(self):
        for i in range(self.poll_num):
            worker = threading.Thread(target=self.run)
            self.threadingList.append(worker)
            worker.start()
    
    def run(self):
        print( '活跃的个数:{}'.format(threading.activeCount()))
        while not self._stop:
            while not self._queue.empty():
                newTask = self._queue.get()
                url = newTask.url
                index = newTask.index
                newTask.searchTxt(url, index)
                self._queue.task_done()

    def add_task(self, task):
        self._queue.put(task)

    def close(self):
       self._queue.join()
       self._stop = True

if __name__ == "__main__":
    poll = Poll(8)
    task_c = Search()
    task = task_c.searchFn()
    length = len(task)
    print(length)
    for index in range(0, length):
        task_real = Search()
        task_url = task[index]
        task_real.url = task_url
        task_real.index = index
        poll.add_task(task_real)
    poll.close()