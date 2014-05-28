import os
import struct

solution_prefix = "sol_"

def list_sol_files(sol_directory):
  lf = []
  for f in os.listdir(sol_directory):
    if f.startswith(solution_prefix):
      filename = os.path.join(sol_directory, f)
      if os.path.isfile(filename):
        lf.append(filename)
  return lf

def send_msg(sock, msg):
  # Prefix each message with a 4-byte length (network byte order)
  msg = struct.pack('>I', len(msg)) + msg
  sock.sendall(msg)

def recv_msg(sock):
  # Read message length and unpack it into an integer
  raw_msglen = recvall(sock, 4)
  if not raw_msglen:
    return None
  msglen = struct.unpack('>I', raw_msglen)[0]
  # Read the message data
  return recvall(sock, msglen)

def recvall(sock, n):
  # Helper function to recv n bytes or return None if EOF is hit
  data = ''
  while len(data) < n:
    packet = sock.recv(n - len(data))
    if not packet:
      return None
    data += packet
  return data


GET_SEED = 0
PUT_SEED = 1
HEARTBEAT = 2
CLAIM = 3
STOP = 4
ELECT = 5

HEARTRATE = 60
TIMEOUT = 181
