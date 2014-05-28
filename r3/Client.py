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
import urllib2

client_id = 0

server_ip  = None
server_port = 12345                # Reserve a port for your service.
server_host = None  #Get server hostname, it returns an array with the hostname in the first element

client_port = 12500
try:
  client_ip = urllib2.urlopen('http://ip.42.pl/raw').read()
except:
  client_ip = '127.0.0.1'
client_hostname = socket.gethostbyaddr(client_ip)[0]

print 'client_ip = ', client_ip
print 'client_hostname =', client_hostname

g_tabu_worker_thread = None
g_sigint = False

counter = 0 

def get_seed():
    global server_ip  
    global server_port
    global server_host
    
    global client_id
    global client_ip
    global client_port
    global client_hostname
    
    request_message = message(GET_SEED, Id=client_id, IP=client_ip, hostname=client_hostname, Port=client_port)
    s = socket.socket()         # Create a socket object

    #Connect to the server
    print "Connecting to Server at %s:%d" % (server_host, server_port)
    s.connect((server_host, server_port))
    #send getseed request to the server
    s.send(request_message.get_json())
    #receive the seed
    recv_message = s.recv(15000).strip()

    s.close()

    decoded_message = message.decode(recv_message)
    # response_message = message(seed)
    return decoded_message.data.strip()

def bind_socket(host, port):
    s = socket.socket()         # Create a socket object
    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.

def accept_connections():
    global g_tabu_worker_thread
    
    global server_ip  
    global server_port
    global server_host
    
    global client_id
    global client_ip
    global client_port
    global client_hostname

    # print 'accept_connections'

    if g_sigint:
      sys.exit(0)

    s = socket.socket()
    s.settimeout(TIMEOUT)
    s.bind((client_hostname, client_port))
    s.listen(1)
    
    try:
        conn, addr = s.accept()
        recv_message  = ""
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            recv_message += chunk
        
        decoded_message = message.decode(recv_message)
        if decoded_message.type == PUT_SEED:
            
            if g_tabu_worker_thread.stopped == False:
              tw.kill_TabuWorker_threads()
              ## blocking on  kill_TabuWorker_threads
              while g_tabu_worker_thread.stopped == False:
                time.sleep(1)

              print 'KILLED g_tabu_worker_thread'

            else:
              print 'g_tabu_worker_thread already stopped'

            seed = decoded_message.data.strip()
            
            tw.init()
            g_tabu_worker_thread = \
              tw.TabuWorker(seed, send_seed_flag=True, 
                            client_id=client_id, client_hostname=client_hostname, client_port=client_port, 
                            server_host=server_host, server_port=server_port, server_ip=server_ip,
                            numWorkers=1, maxSize=102, debugON=False, maxSkipSteps=10)
            g_tabu_worker_thread.start()
            print 'g_tabu_worker_thread started...'

        elif decoded_message.type == HEARTBEAT:
            print "Recieved heartbeat."
            ## TODO is required
            decoded_message = message(HEARTBEAT, data='Beep beep.', Id=client_id, IP=client_ip, hostname=client_hostname, Port=client_port)

    except:
        print sys.exc_info()
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

def main(argv):
    global g_tabu_worker_thread
    global server_ip
    global server_host

    signal.signal(signal.SIGINT, sigint_exit)

    if len(argv) == 2:
      server_ip = argv[1]
    else:
      print 'Defaulting server_ip to 127.0.0.1'
      server_ip = '127.0.0.1'

    server_host = socket.gethostbyaddr(server_ip)[0]
    print 'server_ip =', server_ip
    print 'server_host =', server_host
    
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

main(sys.argv)
