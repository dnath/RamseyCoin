import os
import mod_vault
import time

filenname = 'solution.txt'

f = open(filename)
count = 0

settings_file_name = 'settings.yaml'
# if len(sys.argv) == 2:        
#     settings_file_name = sys.argv[1]
settings_file = open(settings_file_name, 'r')
settings = yaml.load(settings_file)
settings_file.close()

for line in f:
	fw_name = filename + str(count) + '.txt'
	fw = open(fw_name, 'w')
	fw.write(line)
	fw.close()
	
	mod_vault_handler = mod_vault.get_module_handler(settings)
	mod_vault_handler.handle_command(['get', fw_name])
	time.sleep(4)
	
	
	