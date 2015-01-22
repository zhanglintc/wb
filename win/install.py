# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil

# E:\SVN-Space\wb\src
wb_dir = "{0}\src".format(os.path.abspath('..')) # wb.py directory
fr = open('wb.tpl', 'r')
fw = open('wb.cmd', 'w')

line = True
while line:
    line = fr.readline()
    if 'to_be_replaced' in line:
        line = line.replace('to_be_replaced', wb_dir)
    fw.write(line)

fr.close()
fw.close()

shutil.copy('wb.cmd', 'C:\Windows\System32') # copy wb.cmd to system path
os.remove('wb.cmd') # remove wb.cmd

print('')
print('1. "{0}" has been written in "wb.cmd"'.format(wb_dir))
print('2. "wb.cmd" has been copied to "C:\Windows\System32"')
print('')
print('Press any key to close...')

try:
    raw_input()
except:
    pass


