#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
from json_formatter import *# Import json to object translation for counterexample class and message class 


ip_address  = "127.0.0.1"
port = 12345                # Reserve a port for your service.



def get_seed():
	request_message = message(0,"")
	s = socket.socket()         # Create a socket object
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

while True:
	message_type = input("Enter message type:  ")
	if message_type == 0:
		print (get_seed())
	else :
		save_seed("010110010110010110010110010110010110")       