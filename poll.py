## coding: utf-8

import threading
from server import Search

class Poll(object):
    def __init__(self, poll_num = 2):
        self.poll_num = poll_num
        self.threadingList = []
        self.taskList = []
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)
        self.runPoll()
    
    def runPoll(self):
        worker = threading.Thread(target=self.run)
        self.threadingList.append(worker)
        worker.start()
    
    def run(self):
        print( '活跃的个数:{}'.format(threading.activeCount()))
        while True:
            with self.lock:
                while not self.taskList:
                    self.cond.wait()
                newTask = self.taskList.pop(0)
                url = newTask.url
                index = newTask.index
            newTask.searchTxt(url, index)

    def add_task(self, task):
        self.lock.acquire()
        self.taskList.append(task)
        self.cond.notify()
        self.lock.release()
    def close(self):
        pass

if __name__ == "__main__":
    poll = Poll(2)
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