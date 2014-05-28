import time
import threading
import sys
import random
import os
import math
from json_formatter import *
import socket
from tabu import *
from common import *

g_kill_mutex = None
g_kill_flag = False

class TabuWorker(threading.Thread):
  def __init__(self, seed, send_seed_flag=False, 
                      client_id=None, client_hostname=None, client_port=None, 
                      server_host=None, server_port=None, server_ip=None,
                      numWorkers=1, maxSize=102, debugON=False, maxSkipSteps=10):
    super(TabuWorker, self).__init__()

    self.debugON = debugON

    gsize = int(math.sqrt(len(seed)))
    self.seed = [[ 0 if seed[i*gsize + j] == '0' else 1 for j in xrange(gsize)] for i in xrange(gsize)]

    # print 'seed = '
    # print seed

    self.numWorkers = numWorkers
    self.maxSize = maxSize
    self.maxSkipSteps = maxSkipSteps

    self.send_seed_flag = send_seed_flag
    self.client_id = client_id
    self.client_hostname = client_hostname
    self.client_port = client_port

    self.server_host = server_host
    self.server_port = server_port
    self.server_ip = server_ip

    self.stopped = False


  def write_solution(self, graph):
    gsize = len(graph)
    out_filename = 'solution_' + str(gsize) + '_' + str(int(time.time())) + '.txt'
    while os.path.exists(out_filename):
      time.sleep(1)
      out_filename = 'solution_' + str(gsize) + '_' + str(int(time.time())) + '.txt'

    output_file = open(out_filename, 'w')
    for i in xrange(gsize):
      for j in xrange(gsize):
        output_file.write('0' if graph[i][j] == 0 else '1')
    output_file.close()

    self.debug('Solution written : gsize = %d' % gsize)


  def debug(self, msg):
    if self.debugON:
      print str(threading.current_thread()) + ':' + msg

  def run(self):
    global g_kill_mutex
    global g_kill_flag

    skip = random.randint(0, self.maxSkipSteps)

    # Initialize the search space
    graph = copy.deepcopy(self.seed)
    cliqueCount = naiveCliqueCount(graph)
    tabuSize = len(graph)
    tabuDecrement = False

    # Make sure the seed is valid
    if cliqueCount != 0:
      print "Seed is not a counterexample for R(6, 6). Aborting."
      return

    # Create tabu list
    tabuList = OrderedSet.OrderedSet()

    # Start clock
    clockStart = time.clock()
    clockLastSolution = time.clock()

    # Tabu search
    while len(graph) <= self.maxSize:

      # Found a counterexample
      if cliqueCount == 0:

        # Check whether this is a new counterexample
        if tabuDecrement == False:

          # Timestamp solution
          clockFoundSolution = time.clock()

          self.debug("Found counterexample!")
          self.debug("Time elapsed since start: %f" % (clockFoundSolution-clockStart))
          self.debug("Time elapsed since last counterexample: %f" % (clockFoundSolution-clockLastSolution))

          clockLastSolution = clockFoundSolution

          # Print graph
          # printGraph(graph)

          if self.send_seed_flag:
            self.debug('Sending new solution to server...')
            self.save_seed(graph)
          else:
            self.debug('Writing new solution...')
            self.write_solution(graph)

          # TODO: Dispatch graph

        # This is the new seed
        seed = copy.deepcopy(graph)

        # Sanity check
        if naiveCliqueCount(graph) != 0:
          print "Error: Discrepancy between naive and vert0 counts. Aborting."
          # sys.exit(1)
          break

        # Add new vertex to adjacency matrix
        graphDim = len(graph)
        graph.insert(0, [])
        for i in range(graphDim):
          graph[0].append(0)
        for row in graph:
          row.insert(0, 0)

        # Update the clique-count
        cliqueCount = naiveCliqueCount(graph)

        # Reset the tabu list
        tabuList.clear()
        if tabuDecrement == True:
          tabuSize = tabuSize - 1
          tabuDecrement = False
        else:
          tabuSize = len(graph) / self.numWorkers 

        continue

      # Keep looking
      #best = findLocalMinIter(tabuList, graph)
      best = findLocalMinRand(tabuList, graph, self.numWorkers)

      # Could not find couterexample
      if len(best) == 0:

        # Try decreasing the tabu size
        if tabuSize >= 0:
          self.debug("Search failed, resetting tabuSize to %d.\n" % (tabuSize - 1))
          tabuDecrement = True
          graph = copy.deepcopy(seed)
          cliqueCount = 0
          continue

        # Should never get here -- tabu size of zero should run forever...
        print "Could not find counterexample for size %d." % (len(graph))
        return

      # Results of local search
      bestCount = best[0]
      bestI = best[1]
      bestJ = best[2]

      # Keep the best edge-flip
      graph[bestI][bestJ] = 1 - graph[bestI][bestJ]

      # Update the clique count
      cliqueCount = bestCount

      # Taboo this edge
      if tabuSize != 0:
        if len(tabuList) >= tabuSize:
          tabuList.pop(False)
          tabuList.add((bestI, bestJ))

      self.debug("[%d] Flipping (%d, %d), clique count: %d, taboo size: %d" % (len(graph), bestI, bestJ,
        cliqueCount, tabuSize))

      ## check if it needs to be killed
      if skip == 0:
        skip = random.randint(0, self.maxSkipSteps)
        self.debug('skip = ' + str(skip))
        k = False
        # query kill flag
        g_kill_mutex.acquire()
        if g_kill_flag == True:
          k = True
        g_kill_mutex.release()

        if k:
          # check if need to be killed or not
          self.stopped = True
          s = 'Tabu Worker : KILLED'
          print str(threading.current_thread()) + ':' + s
          break
      else:
        skip -= 1

  def save_seed(self, graph):
    gsize = len(graph)
    print 'Saving seed, size = ', gsize
    seed = ''
    for i in xrange(gsize):
      for j in xrange(gsize):
        seed += str(graph[i][j])

    request_message = message(PUT_SEED, seed, self.client_id, self.client_hostname, self.client_port)
    # Create a socket object
    s = socket.socket()
    #Get server hostname, it returns an array with the hostname in the first element
    server_host = socket.gethostbyaddr(self.server_ip)[0] 
    #Connect to the server
    s.connect((self.server_host, self.server_port))
    #send getseed request to the server
    send_msg(s, request_message.get_json())
    s.close()

    self.debug('seed of size = ' + str(gsize) + ' sent')

def init():
  global g_kill_mutex
  global g_kill_flag

  g_kill_flag = False
  g_kill_mutex = threading.Lock()

def kill_TabuWorker_threads():
  global g_kill_mutex
  global g_kill_flag

  g_kill_mutex.acquire()
  g_kill_flag = True
  g_kill_mutex.release()

  # print 'Kill All'
  # print 'END'

if __name__ == '__main__':

  testGraph1 = \
         [[ 0, 0, 1, 0, 1, 0, 1, 0 ],
          [ 0, 0, 1, 0, 1, 0, 1, 0 ],
          [ 0, 0, 0, 0, 1, 0, 1, 0 ],
          [ 0, 0, 0, 0, 1, 0, 1, 0 ],
          [ 0, 0, 0, 0, 0, 0, 1, 0 ], 
          [ 0, 0, 0, 0, 0, 0, 1, 0 ], 
          [ 0, 0, 0, 0, 0, 0, 0, 0 ],
          [ 0, 0, 0, 0, 0, 0, 0, 0 ]]

  seed = ''
  for row in testGraph1:
    for ele in row:
      seed += str(ele)

  print 'seed =', seed

  init()

  n = 1
  t = [TabuWorker(testGraph1, debugON=True, maxSkipSteps=1) for i in xrange(n)]
  for i in xrange(n):
    t[i].start()

  time.sleep(10)
  kill_TabuWorker_threads()
