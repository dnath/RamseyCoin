#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import json					# Import json module


ip_address  = "127.0.0.1"
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
s.send("getseed")
print s.recv(1024)
s.close                     # Close the socket when done



def 