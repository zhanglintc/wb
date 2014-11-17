#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
import os

print('')
print("This tool helps you REMOVE the 'wb' command from your device")
print("It's going to detect your device automatically")
print("If faild or detection not right, please do it manually\n")

choice = None
if 'Linux' in platform.platform():
    while choice != 'y' and choice != 'n':
        choice = raw_input("'Linux' detected, continue?[y/n]").lower()

    if choice == 'y':
        os.system('cd ./linux && python uninstall.py')
    else:
        print('')
        print("uninstall aborted\n")

elif 'Darwin' in platform.platform():
    while choice != 'y' and choice != 'n':
        choice = raw_input("'Mac' detected, continue?[y/n]").lower()

    if choice == 'y':
        os.system('cd ./mac && python uninstall.py')
    else:
        print('')
        print("uninstall aborted\n")

elif 'Windows' in platform.platform():
    while choice != 'y' and choice != 'n':
        choice = raw_input("'Windows' detected, continue?[y/n]").lower()

    if choice == 'y':
        os.system('cd ./win & python uninstall.py')
    else:
        print('')
        print("uninstall aborted\n")

else:
    print("Can't detect your device, please do it by yourself\n")



