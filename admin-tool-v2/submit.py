#! /usr/bin/python
import sys
import os
import mod_vault
import time
import yaml
from datetime import datetime

filename = 'solution.txt'
if len(sys.argv) == 2:        
     filename = sys.argv[1]

f = open(filename)

settings_file_name = 'settings.yaml'
# if len(sys.argv) == 2:        
#     settings_file_name = sys.argv[1]
settings_file = open(settings_file_name, 'r')
settings = yaml.load(settings_file)
settings_file.close()

### skipped 0
skip = 0
print 'skip =', skip
count = -1
for line in f:
	count += 1
	print str(datetime.now()), 'count =', count
	if count < skip:
		continue
	fw_name = filename + '_sol.txt'
	fw = open(fw_name, 'w')
	fw.write(line)
	fw.close()
	
	mod_vault_handler = mod_vault.get_module_handler(settings)
	ret = mod_vault_handler.handle_command(['mint', fw_name])
	while ret is not True:
		print str(datetime.now()), 'Attempt failed ! count =', count
		ret = mod_vault_handler.handle_command(['mint', fw_name])
		time.sleep(3)		
	time.sleep(3)
	
f.close()
	
	
	
