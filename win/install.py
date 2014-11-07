# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil

fr = open('wb.tpl', 'r')
fw = open('wb.cmd', 'w')

line = True
while line:
    line = fr.readline()
    if 'to_be_replaced' in line:
        line = line.replace('to_be_replaced', os.path.abspath('..')+'\src')
    fw.write(line)

fr.close()
fw.close()

shutil.copy('wb.cmd', 'C:\Windows\System32')
os.remove('wb.cmd')

print 'Successfully installed!!!'
print ''
print 'Press any key to close...'
raw_input()