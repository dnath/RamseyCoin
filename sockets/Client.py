#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
from json_formatter import *# Import json to object translation for counterexample class and message class 


server_ip  = "127.0.0.1"
server_port = 12345                # Reserve a port for your service.
client_port = 12500
client_ip = socket.gethostname()

counter = 0 



def get_seed():
	request_message = message(0,"")
	s = socket.socket()         # Create a socket object
	#TODO host should the server IP
	host = socket.gethostname() # Get local machine name
	s.connect((host, port))
	s.send(request_message.get_json())
	seed = s.recv(15000).strip()
	s.close()
	response_message = message(seed)
	return response_message.data.strip()

def save_seed(seed):
	request_message = message(1,seed)
	s = socket.socket()         # Create a socket object
	host = socket.gethostname() # Get local machine name
	s.connect((host, port))
	s.send(request_message.get_json())
	s.close()

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

def main():
	seed  = get_seed()
	thread.start_new_thread(taboo(seed, 1))
 	bind_socket(client_ip,client_port)
 	accept_connections()

