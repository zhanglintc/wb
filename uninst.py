#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
import os

print('')
print("This tool helps you REMOVE the 'wb' command from your device")
print("It's going to detect your device automatically")
print("If faild or detection not right, please do it manually\n")

choice = None
os_info = platform.platform()

# os_type[1]: for folder use
if 'Linux' in os_info:
    os_type = ['Linux', 'linux']
elif 'Darwin' in os_info:
    os_type = ['Mac', 'mac']
elif 'Windows' in os_info:
    os_type = ['Windows', 'win']
else:
    print("Can't detect your device, please do it by yourself\n")
    raw_input()
    sys.exit(0)

while choice != 'y' and choice != 'n':
    choice = raw_input("'{0}' detected, continue?[y/n]".format(os_type[0])).lower() # os_type[0]: for display

if choice == 'y':
    os.system('cd ./{0} && python uninstall.py'.format(os_type[1])) # os_type[1]: for folder use
else:
    print('')
    print("uninstall aborted\n")
    raw_input()
    sys.exit(0)


