# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil

# /Users/lane
gen_path  = os.path.expanduser('~') # your home path

# /Users/lane/.bash_aliases
bash_path = "{}/.bash_aliases".format(gen_path) # your .bash_aliases path

# /Users/lane/temp
temp_path = "{}/temp".format(gen_path) # temp file path

# /Users/lane/Github/wb/src/wb.py
wb_path = "{}/src/wb.py".format(os.path.abspath('..')) # wb.py file path

# alias wb='python /Users/lane/Github/wb/src/wb.py'
alias = "alias wb='python {}'\n".format(wb_path) # the alias command

# make sure there is .bash_aliases
os.system('touch {}'.format(bash_path))

# open files
fr = open(bash_path, 'r')
fw = open(temp_path, 'w')

line = True; add_alias = True
while line:
    line = fr.readline()
    fw.write(line)
    if 'wb.py' in line: # if wb.py already in .bash_aliases, no need to add alias command
        add_alias = False
        intalled_command = line
    else:
        pass

if add_alias: # if True, write alias command at the end of the file
    fw.write(alias)
else:
    pass

fr.close()
fw.close()

shutil.copy(temp_path, bash_path) # replace .bash_aliases by temp file
os.remove(temp_path) # delete temp file

print('')
if add_alias:
    print("The command below:\n\n  {}\n\nis successfully added to '.bash_aliases'\n".format(alias[:-1]))
else:
    print("The command below:\n\n  {}\n\nis already exist, installing has canceled with nothing happen\n".format(intalled_command[:-1]))

print('')
print("please type 'source ~/.bash_aliases' or restart your bash")
print("to make this installment take effect\n")
print("press any key to quit...\n")

try:
    raw_input()
except:
    pass


