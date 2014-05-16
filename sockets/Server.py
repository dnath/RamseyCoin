#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
from json_formatter import *# Import json to object translation for counterexample class and message class 
from os import listdir
from os.path import isfile, join
import math

solution_directory = "solutions/" #define solution directory where there is a file for every counterexample size.
solution_prefix = "sol_"
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.

def list_file(directory):
	onlyfiles = [ f for f in listdir(directory) if isfile(join(directory,f)) ]
	return onlyfiles

def handle_request(connection, message_json):
	request_message = message(message_json)
	type = request_message.type

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




while True:
   c, addr = s.accept()     # Establish connection with client.
   message_json = c.recv(15000)
   print(message_json)
   handle_request(c, message_json)