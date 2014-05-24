#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
from json_formatter import *# Import json to object translation for counterexample class and message class 
from os import listdir
from os.path import isfile, join
import math

#global variables
Id = 1
clients_file = "clients.txt"
solution_directory = "solutions/" #define solution directory where there is a file for every counterexample size.
solution_prefix = "sol_"
IP = "127.0.0.1"
#server_hostname = socket.gethostname() # Get local machine name
server_hostname = "localhost"
server_port = 12345                # Reserve a port for your service.

# Dictionary of client node which are running taboo search.
# This dictionary should be saved on some presistent storage S3
# It will be used in case of schedular failer
client_dictionary = {}

#Any node in the system has and Id, IP and port. 
class Node: 
    def __init__(self, Id, IP, Port):
        self.Id = Id
        self.IP = IP
        self.Port = Port

def list_file(directory):
    onlyfiles = [ f for f in listdir(directory) if isfile(join(directory,f)) ]
    return onlyfiles

def handle_request(c, message_json):
    request_message = message(message_json)
    type = request_message.type

    #get_seed, should be the first message from the client when it joins the system
    if type == 0: #get_seed
        print "Recieved 'get_seed' request from client"
        #add client to client list
        clientNode = Node(request_message.Id,request_message.IP,request_message.Port)
        client_dictionary[clientNode.Id] = clientNode
        #save clients list
        save_clients_file (clients_file)
        #list solution files
        file_list = list_file(solution_directory)
        file_list.sort()
        if(len(file_list)!=0):
            f = open(solution_directory + file_list[len(file_list)-1],"r")
            line = f.readline()
            f.close()
            response_message = message (2,line)
            c.send(response_message.get_json())
        else:
            c.send("no counterexample available")
        c.close()
    elif type == 1: #save_counter_example
        print "Recieved 'save_counterexample' request from client"
        data = request_message.data
        size = math.sqrt(len(data))
        filename = solution_directory + solution_prefix + str(size)
        file_list = list_file(solution_directory)
        f = open(filename, 'a')
        f.write(data + "\n")
        f.close()
        c.close()
        if filename not in file_list:
            #new solution size
            #broadcast this solution to every one
            bcmessage = message(2,data,Id,IP,server_port)
            broad_cast(bcmessage)
    #elif type == 2: # Heartbeat acknowledgement 



def bind_socket(host,port):
    s = socket.socket()         # Create a socket object
    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.
    return s

def accept_connections(s):
    while True:
        c, addr = s.accept()     # Establish connection with client.
        message_json = c.recv(15000)
        print(message_json)
        try:
            thread.start_new_thread( handle_request, (c, message_json))
        except:
            print "Error: unable to start thread"



# Read clients' connection data from file to a dictionary
def read_clients_file(file_name):
    fp = open(file_name,"r")
    #line in the form, clientID, IP and Port
    clientStrings = fp.readlines()
    fp.close()
    clients = {}
    for clientString in clientStrings:
        clientStringPart = clientString.split(",")
        client = Node(clientStringPart[0],clientStringPart[1],clientStringPart[2])
        clients [client.Id] = client

    return clients

#Save clients' connection data to clients file
def save_clients_file(file_name,clients):
    fp = open(file_name,"w")

    for key in clients.keys():
        clientObject = clients[key]
        clientString = clientObject.Id+","+clientObject.IP+","+clientObject.Port+"\n"
        fp.write(clientString)
    fp.close()

#not used
#Add new client connection data to clients file
def add_new_client(file_name, client):
    fp = open(file_name,"a")
    clientString = clientObject.Id+","+clientObject.IP+","+clientObject.Port+"\n"
    fp.write(clientString)
    fp.close()

def broad_cast(message):
    for key in client_dictionary.keys():
        client = client_dictionary[key]
        s = socket.socket()         # Create a socket object
        host = socket.gethostbyaddr(client.IP)[0]
        s.connect((host, server_port))
        s.send(message)
        s.close() 



def main ():
    print "Starting RamseyCoin Server..."
    #Open a socket 
    sock = bind_socket(server_hostname, server_port)
    print "listening on %s:%d." % (server_hostname, server_port)
    #accept client messages
    accept_connections(sock)

#start server process
main()
