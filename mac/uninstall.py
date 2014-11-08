# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil, sys
import getpass

usr = getpass.getuser()

gen_path = '/Users/' + usr
bash_path = gen_path + '/.bash_profile'
tmp_path = gen_path + '/tmp'


fr = open(bash_path, 'r')
fw = open(tmp_path, 'w')

line = True; add_alias = True
while line:
    line = fr.readline()
    if 'wb.py' not in line:
        fw.write(line)
    else:
        pass

fr.close()
fw.close()

shutil.copy(tmp_path, bash_path)
os.remove(tmp_path)

print 'Successfully uninstalled!!!'
print ''
print 'Press any key to close...\n'
try:
    raw_input()
except:
    pass