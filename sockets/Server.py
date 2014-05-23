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
host_name = socket.gethostname() # Get local machine name
port_number = 12345                # Reserve a port for your service.

# Dictionary of client node which are running taboo search.
# This dictionary should be saved on some presistent storage S3
# It will be used in case of schedular failer
client_dictionary = {}






def list_file(directory):
	onlyfiles = [ f for f in listdir(directory) if isfile(join(directory,f)) ]
	return onlyfiles

def handle_request(message_json):
	request_message = message(message_json)
	type = request_message.type

	#get_seed, should be the first message from the client when it joins the system
	if type == 0: #get_seed

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
		data = request_message.data
		size = math.sqrt(len(data))
		filename = solution_directory + solution_prefix + str(size)
		f = open(filename, 'a')
		f.write(data + "\n")
		f.close()
		c.close()
	#elif type == 2: # Heartbeat acknowledgement 



def bind_socket(host,port):
	s = socket.socket()         # Create a socket object
	s.bind((host, port))        # Bind to the port
	s.listen(5)                 # Now wait for client connection.

def accept_connections():
	while True:
		c, addr = s.accept()     # Establish connection with client.
		message_json = c.recv(15000)
		print(message_json)
		try:
		   	thread.start_new_thread( handle_request, ("Thread-1", 2, ))
		except:
	   		print "Error: unable to start thread"

	   handle_request(c, message_json)


#Any node in the system has and Id, IP and port. 
class Node: 
	def __init__(self, Id, IP, Port):
		self.Id = Id
		self.IP = IP
		self.Port = Port


# Read clients' connection data from file to a dictionary
def read_clients_file(file_name):
	fp = open(file_name,"r")
	#line in the form, clientID, IP and Port
	clientStrings = fp.readlines()
	fp.close()
	clients = {}
	for clientString in clientStrings:
		clientStringPart = clientString.split(",")
		client = new Node(clientStringPart[0],clientStringPart[1],clientStringPart[2])
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


#Add new client connection data to clients file
def add_new_client(file_name, client):
	fp = open(file_name,"a")
	clientString = clientObject.Id+","+clientObject.IP+","+clientObject.Port+"\n"
	fp.write(clientString)
	fp.close()


def main ():
	#Open a socket 
	bind_socket()
	#accept client messages






#start server process
main()