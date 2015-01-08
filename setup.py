#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
import os, sys

print("Please MAKE SURE you are using Python 2.7.9 (not Python3).")
print("Otherwise Errors would be occured.")

try:
    input()
except:
    pass

print('')
print("This tool helps you ADD the 'wb' command to your device")
print("It's going to detect your device automatically")
print("If faild or detection not right, please do it manually\n")

choice = None
if 'Linux' in platform.platform():
    while choice != 'y' and choice != 'n':
        choice = raw_input("'Linux' detected, continue?[y/n]").lower()

    if choice == 'y':
        os.system('cd ./linux && python install.py')
    else:
        print('')
        print("setup aborted\n")
        raw_input()
        sys.exit(0)

elif 'Darwin' in platform.platform():
    while choice != 'y' and choice != 'n':
        choice = raw_input("'Mac' detected, continue?[y/n]").lower()

    if choice == 'y':
        os.system('cd ./mac && python install.py')
    else:
        print('')
        print("setup aborted\n")
        raw_input()
        sys.exit(0)

elif 'Windows' in platform.platform():
    while choice != 'y' and choice != 'n':
        choice = raw_input("'Windows' detected, continue?[y/n]").lower()

    if choice == 'y':
        os.system('cd ./win & python install.py')
    else:
        print('')
        print("setup aborted\n")
        raw_input()
        sys.exit(0)

else:
    print("Can't detect your device, please do it by yourself\n")

print("Now we are going to install dependent modules:\n")
os.system('python ./bin/pip.exe install -r requirements.txt')

print('')
print("Completed, press any key to close...")
print("(If any exception occured, please do it manually)")
raw_input()


