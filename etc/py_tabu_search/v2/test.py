import time
import threading
import sys
import random

class TabuSearchThread(threading.Thread):
  def __init__(self, seed):
      super(TabuSearchThread, self).__init__()
      self._stop = threading.Event()
      self.seed = seed

  def run(self):
    global kill_mutex
    global kill

    while True:
      k = False
      # query kill flag
      kill_mutex.acquire()
      if kill == True:
        k = True
      kill_mutex.release()

      if k:
        # check if need to be killed or not
        s = str(self.seed) + ' : KILLED'
        print s 
        sys.exit(0)
      else:
        # do a little work
        s = str(self.seed) + ' : alive'
        print s
        time.sleep(random.random()*10)
    


if __name__ == '__main__':
  global kill_mutex
  global kill

  kill = False
  kill_mutex = threading.Lock()
  
  n = 10
  t = [TabuSearchThread(str(i)) for i in xrange(n)]
  for i in xrange(n):
    t[i].start()

  time.sleep(20)
  
  kill_mutex.acquire()
  kill = True
  kill_mutex.release()
  
  print 'Kill All'
  # time.sleep(3)
  print 'END'
