#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
from json_formatter import *# Import json to object translation for counterexample class and message class 
from tabu import tabu
import thread
import math
import time
import tabu_worker as tw
from common import *

client_id = 2

server_ip  = "127.0.1.1"
server_port = 12345                # Reserve a port for your service.
server_host = socket.gethostbyaddr(server_ip)[0]  #Get server hostname, it returns an array with the hostname in the first element

client_port = 12500
client_hostname = socket.gethostname()

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


def save_seed(seed):
    request_message = message(1, seed, client_id, client_hostname, client_port)
    s = socket.socket()         # Create a socket object
    #Connect to the server
    s.connect((server_host, server_port))
    #send getseed request to the server
    s.send(request_message.get_json())
    s.close()

def bind_socket(host,port):
    s = socket.socket()         # Create a socket object
    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.

def accept_connections():
    s = socket.socket()
    s.settimeout(TIMEOUT)
    s.bind((client_hostname, client_port))
    s.listen(1)
    conn, addr = s.accept()
    message_json  = ""
    while True:
        chunk = c.recv(1024)
        if not chunk:
            break
        message_json += chunk
    resp = message(message_json)
    if resp.type == PUT_SEED:
        ## FIXME kill_TabuWorker_threads should block
        tw.kill_TabuWorker_threads()
        seed = resp.data.strip()
        tw.init()
        tabu_worker_thread = tw.TabuWorker(seed, debugON=False, maxSkipSteps=10)
        tabu_worker_thread.start()

    elif resp.type == HEARTBEAT:
        resp = message(HEARTBEET, "Beep beep.", client_id, client_ip, client_port)
        s.send(resp.get_json())

    s.close()


def main():
    print "Starting RamseyCoin Client..."
    print "> Trying on %s:%d" % (client_hostname, client_port)
    seed = get_seed()
    print "seed =", seed
    print "Got seed, forking tabu search on separate thread..."
    # start taboo search thread
    tw.init()
    tabu_worker_thread = tw.TabuWorker(seed, debugON=False, maxSkipSteps=10)
    tabu_worker_thread.start()
    # now listen for messages from Server
    while True:
        accept_connections()
    #time.sleep(5)
    #tw.kill_TabuWorker_threads()

    # bind a socket in the client for furthet communication
    # bind_socket(client_hostname, client_port)
    # listen for connections from the server
    # accept_connections()

main()
