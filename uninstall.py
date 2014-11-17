#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
import os

if 'Linux' in platform.platform():
    print('Linux detected\n')
    os.system('cd ./linux & python uninstall.py')

if 'Darwin' in platform.platform():
    print('Mac detected\n')
    os.system('cd ./mac && python uninstall.py')

if 'Windows' in platform.platform():
    print('Windows detected\n')
    os.system('cd ./win & python uninstall.py')
