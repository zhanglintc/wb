#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
import os

if 'Linux' in platform.platform():
    print('Linux detected\n')
    os.system('cd ./linux & python install.py')

if 'Darwin' in platform.platform():
    print('Mac detected\n')
    os.system('cd ./mac && python install.py')

if 'Windows' in platform.platform():
    print('Windows detected\n')
    os.system('cd ./win & python install.py')
