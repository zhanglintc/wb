# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil

# /Users/lane
gen_path  = os.path.expanduser('~') # your home path

# /Users/lane/.bash_profile
bash_path = "{0}/.bash_profile".format(gen_path) # your .bash_profile path

# /Users/lane/temp
temp_path = "{0}/temp".format(gen_path) # temp file path

# /Users/lane/Github/wb/src/wb.py
wb_path = "{0}/src/wb.py".format(os.path.abspath('..')) # wb.py file path

# alias wb='python /Users/lane/Github/wb/src/wb.py'
alias = "alias wb='python {0}'\n".format(wb_path) # the alias command

# make sure .bash_profile is exist
os.system('touch {0}'.format(bash_path))

# open files
fr = open(bash_path, 'r')
fw = open(temp_path, 'w')

line = True; add_alias = True
while line:
    line = fr.readline()
    fw.write(line)
    if 'wb.py' in line: # if wb.py already in .bash_profile, no need to add alias command
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

shutil.copy(temp_path, bash_path) # replace .bash_profile by temp file
os.remove(temp_path) # delete temp file

print('')
if add_alias:
    print("The command below:\n\n  {0}\n\nis successfully added to .'bash_profile'\n".format(alias[:-1]))
else:
    print("The command below:\n\n  {0}\n\nis already exist, installing has canceled with nothing happen\n".format(intalled_command[:-1]))

print('')
print("please TYPE 'source ~/.bash_profile' or RESTART your terminal")
print("to make this installment take effect\n")
print("press any key to quit...\n")

try:
    raw_input()
except:
    pass


