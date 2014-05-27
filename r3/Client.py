#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
from json_formatter import *# Import json to object translation for counterexample class and message class 
from tabu import tabu
import thread
import math
import time
import tabu_worker as tw
from common import *
import signal
import sys
import threading

client_id = 2

server_ip  = "127.0.0.1"
server_port = 12345                # Reserve a port for your service.
server_host = socket.gethostbyaddr(server_ip)[0]  #Get server hostname, it returns an array with the hostname in the first element

client_port = 12500
client_hostname = socket.gethostname()
client_ip = socket.gethostbyname(client_hostname)
g_tabu_worker_thread = None
g_sigint = False

counter = 0 

def get_seed():
    request_message = message(0, "", client_id, client_hostname, client_port)
    s = socket.socket()         # Create a socket object

    #Connect to the server
    print "Connecting to Server at %s:%d" % (server_host, server_port)
    s.connect((server_host, server_port))
    #send getseed request to the server
    s.send(request_message.get_json())
    #receive the seed
    seed = s.recv(15000).strip()
    s.close()
    response_message = message(seed)
    return response_message.data.strip()

def bind_socket(host,port):
    s = socket.socket()         # Create a socket object
    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.

def accept_connections():
    global g_tabu_worker_thread

    # print 'accept_connections'

    if g_sigint:
      sys.exit(0)

    s = socket.socket()
    s.settimeout(TIMEOUT)
    s.bind((client_hostname, client_port))
    s.listen(1)
    try:
        conn, addr = s.accept()
        message_json  = ""
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            message_json += chunk
        resp = message(message_json)
        if resp.type == PUT_SEED:
            
            if g_tabu_worker_thread.stopped == False:
              tw.kill_TabuWorker_threads()
              ## blocking on  kill_TabuWorker_threads
              while g_tabu_worker_thread.stopped == False:
                time.sleep(1)

              print 'KILLED g_tabu_worker_thread'

            else:
              print 'g_tabu_worker_thread already stopped'

            seed = resp.data.strip()
            
            tw.init()
            g_tabu_worker_thread = \
              tw.TabuWorker(seed, send_seed_flag=True, 
                            client_id=client_id, client_hostname=client_hostname, client_port=client_port, 
                            server_host=server_host, server_port=server_port, server_ip=server_ip,
                            numWorkers=1, maxSize=102, debugON=False, maxSkipSteps=10)
            g_tabu_worker_thread.start()
            print 'g_tabu_worker_thread started...'

        elif resp.type == HEARTBEAT:
            print "Recieved heartbeat."
            resp = message(HEARTBEAT, "Beep beep.", client_id, client_ip, client_port)
            s.send(resp.get_json())
            print "Sent heartbeat ACK."

    except:
        print "Socket timed out."
    s.close()

def sigint_exit(signum, frame):
  global g_sigint
  global g_tabu_worker_thread

  if threading.current_thread().__class__.__name__ == '_MainThread':
    print 'handling SIGINT'

    g_sigint = True

    if g_tabu_worker_thread is None:
      sys.exit(0)
    if g_tabu_worker_thread.stopped:
      # print 'g_tabu_worker_thread.isAlive() =', g_tabu_worker_thread.isAlive()
      sys.exit(0)

    tw.kill_TabuWorker_threads()

    ## blocking on  kill_TabuWorker_threads
    while g_tabu_worker_thread.stopped == False:
      time.sleep(1)

    print 'KILLED g_tabu_worker_thread'
    sys.exit(0)

def main():
    global g_tabu_worker_thread


    signal.signal(signal.SIGINT, sigint_exit)
    
    print "Starting RamseyCoin Client..."
    print "> Trying on %s:%d" % (client_hostname, client_port)
    
    seed = get_seed()
    print "seed =", seed
    print "Got seed, forking tabu search on separate thread..."
    
    ## start taboo search thread
    tw.init()
    g_tabu_worker_thread = \
        tw.TabuWorker(seed, send_seed_flag=True, 
                      client_id=client_id, client_hostname=client_hostname, client_port=client_port, 
                      server_host=server_host, server_port=server_port, server_ip=server_ip,
                      numWorkers=1, maxSize=102, debugON=False, maxSkipSteps=10)
    g_tabu_worker_thread.start()

    # now listen for messages from Server
    while True:
        accept_connections()
    
    # time.sleep(5)
    # tw.kill_TabuWorker_threads()

main()
