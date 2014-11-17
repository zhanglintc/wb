# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil

# /Users/lane
gen_path  = os.path.expanduser('~') # your home path

# /Users/lane/.bash_aliases
bash_path = "{}/.bash_aliases".format(gen_path) # your .bash_aliases path

# /Users/lane/temp
temp_path = "{}/temp".format(gen_path) # temp file path

fr = open(bash_path, 'r')
fw = open(temp_path, 'w')

line = True; install_command = False
while line:
    line = fr.readline()
    if 'wb.py' not in line: # if this line do not contain wb.py, write it to file
        fw.write(line)
    else: # else jump it, but store to print
        install_command = line

fr.close()
fw.close()

shutil.copy(temp_path, bash_path) # replace .bash_aliases by temp file
os.remove(temp_path) # delete temp file

if install_command:
    print("The command below:\n\n  {}\n\nis successfully removed from '.bash_aliases'\n".format(install_command[:-1]))
else:
    print("Well, there is nothing to delete\n")

print("press any key to quit...\n")

try:
    raw_input()
except:
    pass


