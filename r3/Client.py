#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
from json_formatter import *# Import json to object translation for counterexample class and message class 
from tabu import tabu
import thread
import math

client_id = 2
server_ip  = "127.0.0.1"
server_port = 12345                # Reserve a port for your service.
client_port = 12500
client_hostname = socket.gethostname()

counter = 0 



def get_seed():
    request_message = message(0,"",client_id,client_hostname,client_port)
    s = socket.socket()         # Create a socket object

    #Get server hostname, it returns an array with the hostname in the first element
    server_host = socket.gethostbyaddr(server_ip)[0] 
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
    request_message = message(1,seed,client_id,client_hostname,client_port)
    s = socket.socket()         # Create a socket object
    #Get server hostname, it returns an array with the hostname in the first element
    server_host = socket.gethostbyaddr(server_ip)[0] 
    #Connect to the server
    s.connect((server_host, server_port))
    #send getseed request to the server
    s.send(request_message.get_json())
    s.close()

def bind_socket(host,port):
    s = socket.socket()         # Create a socket object
    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.


#handle requests from the server
def handle_request(request_json):
    response_message = message(request_json)

def accept_connections():
    while True:
        c, addr = s.accept()     # Establish connection with client.
        message_json = c.recv(15000)
        try:
            thread.start_new_thread(handle_request, (message_json))
        except:
            print "Error: unable to start thread"

def main():
    print "Starting RamseyCoin Client..."
    print "> listening on %s:%d" % (client_hostname, client_port)
    seed = get_seed()
    print "seed =", seed
    print "Got seed, forking tabu search on separate thread..."
    #start taboo search thread
    # thread.start_new_thread(tabu(seed, 1))
    # #bind a socket in the client for furthet communication
    # bind_socket(client_hostname,client_port)
    # #listen for connections from the server
    # accept_connections()

main()
