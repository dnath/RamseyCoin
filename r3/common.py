import os

def list_files(directory):
  return [ f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f)) ]

GET_SEED = 0
PUT_SEED = 1
HEARTBEAT = 2

TIMEOUT = 180
