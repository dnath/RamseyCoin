#!/usr/bin/python           

import socket 
import time
from json_formatter import *
import os
import thread
import math
from common import *
import urllib2
import threading


#global variables

DEBUG = True
Id = 1
clients_file = "clients.txt"
solution_directory = "solutions" #define solution directory where there is a file for every counterexample size.

# server ip
# IP = '127.0.0.1'
try:
  IP = urllib2.urlopen('http://ip.42.pl/raw').read()
except:
  IP = '127.0.0.1'

print 'server ip =', IP
server_hostname = socket.gethostbyaddr(IP)[0]
print 'server_hostname =', server_hostname
# server_hostname = socket.gethostname() # Get local machine name
server_port = 12345                # Reserve a port for your service.
heartbeat_port = 12346

g_sol_file_mutex = threading.Lock()
g_client_file_mutex = threading.Lock()
g_client_maxid_mutex = threading.Lock()

g_client_maxid = 0

# Dictionary of client node which are running taboo search.
# This dictionary should be saved on some presistent storage S3
# It will be used in case of schedular failer
client_dictionary = {}

def debug(msg):
  if DEBUG:
    print msg

#Any node in the system has and Id, IP and port. 
class Node: 
    def __init__(self, Id, IP, Port):
        self.Id = Id
        self.IP = IP
        self.Port = Port

def heartbeat():
    s = socket.socket()
    while True:
        print "Sending heartbeat..."
        bcmessage = message(HEARTBEAT, data='Beep.', Id=Id, IP=IP, hostname=server_hostname, Port=server_port)
        broadcast_with_timeout(bcmessage.get_json())
        time.sleep(HEARTRATE)

def handle_PUT_SEED(c, request_message):
  global g_write_mutex

  print "Recieved 'save_counterexample' request from client"
  data = request_message.data
  size = int(math.sqrt(len(data)))
  print 'size =', size
  
  # to maintain sorting
  str_size = '%.3d' % size
  
  filename = os.path.join(solution_directory, solution_prefix + str_size + '.0')
  print '\nfilename =', filename
  sol_file_list = list_sol_files(solution_directory)
  # print sol_file_list
  
  g_sol_file_mutex.acquire()
  
  f = open(filename, 'a')
  f.write(data + "\n")
  f.close()
  c.close()

  g_sol_file_mutex.release()
  
  if filename not in sol_file_list:
    #new solution size
    #broadcast this solution to every one
    bc_message = message(PUT_SEED, data=data, Id=Id, IP=IP, hostname=server_hostname, Port=server_port)
    broadcast(bc_message.get_json())

def handle_GET_SEED(c, decoded_message):
  global g_write_mutex
  global g_client_maxid_mutex
  global g_client_maxid

  print "Recieved 'get_seed' request from client"

  g_client_maxid_mutex.acquire()
  g_client_maxid += 1
  g_client_maxid_mutex.release()

  #add client to client list
  clientNode = Node(g_client_maxid, decoded_message.IP, decoded_message.Port)

  #save clients list
  add_new_client(clients_file, clientNode)
  #list solution files
  file_list = list_sol_files(solution_directory)
  file_list.sort()
  # print file_list
  if(len(file_list) != 0):
    filename = file_list[len(file_list)-1]
    print '\nsolution filename = ', filename
    
    g_sol_file_mutex.acquire()
    
    f = open(filename, 'r')
    line = f.readline()
    f.close()
    
    g_sol_file_mutex.release()

    # send PUT_SEED message
    response_message = message (PUT_SEED, data=line)
    c.send(response_message.get_json())
  else:
    c.send("no counterexample available")
  c.close()

def handle_request(c, recv_message):
    # print '\nmessage =\n', message
    # print
    decoded_message = message.decode(recv_message)
    # print '\decoded_message =\n', decoded_message
    # print
    
    # get_seed, should be the first message from the client when it joins the system
    # get_seed
    if decoded_message.type == GET_SEED:
      debug('handling GET_SEED')
      handle_GET_SEED(c, decoded_message)  

    # save_counter_example
    # save seed == PUT_SEED in server
    elif decoded_message.type == PUT_SEED: 
      debug('handling PUT_SEED')
      handle_PUT_SEED(c, decoded_message)

    #elif type == 2: # Heartbeat acknowledgement 



def bind_socket(host,port):
    s = socket.socket()         # Create a socket object
    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.
    return s

def accept_connections(s):
    while True:
        c, addr = s.accept()     # Establish connection with client.
        recv_message = c.recv(15000)
        # print(message_json)
        thread.start_new_thread(handle_request, (c, recv_message))
        #try:
            #thread.start_new_thread( handle_request, (c, message_json))
        #except:
            #print "Error: unable to start thread"



# Read clients' connection data from file to a dictionary
def read_clients_file(file_name):
    g_client_file_mutex.acquire()

    fp = open(file_name, 'r')
    #line in the form, clientID, IP and Port
    clientStrings = fp.readlines()
    fp.close()

    g_client_file_mutex.release()

    clients = {}
    for clientString in clientStrings:
        clientStringPart = clientString.split(",")
        client = Node(clientStringPart[0], clientStringPart[1], clientStringPart[2])
        clients[client.Id] = client

    return clients

#Save clients' connection data to clients file
def save_clients_file(file_name, clients):
    g_client_file_mutex.acquire()

    fp = open(file_name,"w")

    for key in clients.keys():
        clientObject = clients[key]
        clientString = str(clientObject.Id) + "," + clientObject.IP + "," + str(clientObject.Port) + "\n"
        fp.write(clientString)
    fp.close()

    g_client_file_mutex.release()

#not used
#Add new client connection data to clients file
def add_new_client(file_name, clientNode):
    g_client_file_mutex.acquire()

    fp = open(file_name, 'a')
    clientString = clientNode.Id + "," + clientNode.IP + "," + clientNode.Port + "\n"
    fp.write(clientString)
    fp.close()

    g_client_file_mutex.release()

def broadcast_with_timeout(message):
    # print 'Broadcast...\n', message 
    for key in client_dictionary.keys():
        client = client_dictionary[key]
        s = socket.socket()         # Create a socket object
        s.settimeout(TIMEOUT)
        host = socket.gethostbyaddr(client.IP)[0]
        try:
            s.connect((host, client.Port))
            s.send(message)
            s.close() 
        except:
            print "Could not connect to %s:%d." % (host, client.Port)

def broadcast(message):
    # print 'Broadcast...\n', message 
    for key in client_dictionary.keys():
        print 'Sending to ', client_dictionary[key].IP
        client = client_dictionary[key]
        s = socket.socket()         # Create a socket object
        host = socket.gethostbyaddr(client.IP)[0]
        try:
            s.connect((host, client.Port))
            s.send(message)
            s.close() 
        except:
            print "Could not connect to %s:%d." % (host, client.Port)

def main():
    if os.path.exists(clients_file):
      os.remove(clients_file)

    print "Starting RamseyCoin Server..."
    # Start the heartbeat
    thread.start_new_thread(heartbeat, ())
    # Open a socket 
    sock = bind_socket(server_hostname, server_port)
    print "listening on %s:%d." % (server_hostname, server_port)
    #accept client messages
    accept_connections(sock)

#start server process
main()
