# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os

os.remove('C:\Windows\System32\wb.cmd')

print('')
print('"wb.cmd" has been removed from "C:\Windows\System32"')
print('')
print('Press any key to close...')

try:
    raw_input()
except:
    pass


