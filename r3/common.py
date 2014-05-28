import os

solution_prefix = "sol_"

def list_sol_files(sol_directory):
  lf = []
  for f in os.listdir(sol_directory):
    if f.startswith(solution_prefix):
      filename = os.path.join(sol_directory, f)
      if os.path.isfile(filename):
        lf.append(filename)
  return lf


GET_SEED = 0
PUT_SEED = 1
HEARTBEAT = 2

HEARTRATE = 60
TIMEOUT = 181
