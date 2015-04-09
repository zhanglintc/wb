#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Intro:
  Supply all defines and global varibles.

Author:
  Lane(zhanglintc)
"""

from http import *
from affix import *
from sdk import Client, JsonDict
import sys, os
import pickle
import getpass
import argparse
import urllib, urllib2
import configparser
import platform
import sqlite3
import webbrowser
try:
    import tkFileDialog
    is_TKinter_exist = True
except:
    is_TKinter_exist = False

# get version
version = sys.version[0]
input = raw_input if version == '2' else input

# get OS information
global_plat = platform.platform()
if 'Linux' in global_plat:
    global_plat = 'Lin'
elif 'Darwin' in global_plat:
    global_plat = 'Mac'
elif 'Windows' in global_plat:
    global_plat = 'Win'
else:
    global_plat = None

# set path
TOKEN_PATH    = sys.path[0] + '/token'
CONFIG_PATH   = sys.path[0] + '/config.ini'
DATABASE_PATH = sys.path[0] + '/data.db'

# read config.ini
config = configparser.ConfigParser()
config.read(CONFIG_PATH)
API_KEY      = config['Weibo']['API_KEY']
API_SECRET   = config['Weibo']['API_SECRET']
REDIRECT_URI = config['Weibo']['REDIRECT_URI']

# global constant
CONST_ENCODE_MIN = 0
CONST_UTF8 = 1
CONST_GBK  = 2
CONST_ENCODE_MAX = CONST_GBK + 1
CONST_WRONG_ENCODE = 0xffff


