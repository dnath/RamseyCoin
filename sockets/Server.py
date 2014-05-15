#!/usr/bin/python           # This is server.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   message_json = c.recv(15000)
   handle_request(c, message_json)
   print 'Got connection from', addr
   c.send('Thank you for connecting')
   c.close()                # Close the connection

def handle_request(connection, message_json):
	message = json.loads(message_json)
	type = message["type"]

	if type == 0: #get_seed
		
	elif type == 1: #save_counter_example

	#elif type == 2: # Heartbeat acknowledgement 


