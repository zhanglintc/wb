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
    fw.write(line)
    if 'wb.py' in line:
        add_alias = False
    else:
        pass

wb_path = os.path.abspath('..') + '/src/wb.py'
alias = "alias wb=\'python " + wb_path + "\'" + '\n'

if add_alias:
    fw.write(alias)
else:
    pass

fr.close()
fw.close()

shutil.copy(tmp_path, bash_path)
os.remove(tmp_path)

print 'Successfully installed!!!'
print ''
print 'Press any key to close...'
raw_input()