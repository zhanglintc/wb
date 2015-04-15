#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Intro:
  A module which contains some small functions.

Author:
  Lane(zhanglintc)
"""

from __future__ import print_function
from defs import *
import defs
import ctypes, re, platform

class ColorPrint:
    """
    See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winprog/winprog/windows_api_reference.asp
    for information on Windows APIs. - www.sharejs.com
    """

    STD_INPUT_HANDLE     = -10
    STD_OUTPUT_HANDLE    = -11
    STD_ERROR_HANDLE     = -12

    FOREGROUND_BLACK     = 0x00
    FOREGROUND_BLUE      = 0x01 # text color contains blue.
    FOREGROUND_GREEN     = 0x02 # text color contains green.
    FOREGROUND_RED       = 0x04 # text color contains red.
    FOREGROUND_INTENSITY = 0x08 # text color is intensified.

    BACKGROUND_BLUE      = 0x10 # background color contains blue.
    BACKGROUND_GREEN     = 0x20 # background color contains green.
    BACKGROUND_RED       = 0x40 # background color contains red.
    BACKGROUND_INTENSITY = 0x80 # background color is intensified.

    if 'Windows' in platform.platform():
        std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    else:
        std_out_handle = None
    
    def set_cmd_color(self, color, handle=std_out_handle):
        """
        (color) -> bit
        Example: set_cmd_color(self.FOREGROUND_RED | self.FOREGROUND_GREEN | self.FOREGROUND_BLUE | self.FOREGROUND_INTENSITY)
        """

        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bool
    
    def reset_color(self):
        self.set_cmd_color(self.FOREGROUND_RED | self.FOREGROUND_GREEN | self.FOREGROUND_BLUE)
    
    def print_red_text(self, print_text):
        if 'Windows' in platform.platform():
            self.set_cmd_color(self.FOREGROUND_RED | self.FOREGROUND_INTENSITY)
            print(print_text, end = '')
            self.reset_color()

        else:
            print('\033[91m' + print_text + '\033[0m', end = '')
        
    def print_green_text(self, print_text):
        if 'Windows' in platform.platform():
            self.set_cmd_color(self.FOREGROUND_GREEN | self.FOREGROUND_INTENSITY)
            print(print_text, end = '')
            self.reset_color()

        else:
            print('\033[92m' + print_text + '\033[0m', end = '')
    
    def print_blue_text(self, print_text):
        if 'Windows' in platform.platform():
            self.set_cmd_color(self.FOREGROUND_BLUE | self.FOREGROUND_INTENSITY)
            print(print_text, end = '')
            self.reset_color()

        else:
            print('\033[96m' + print_text + '\033[0m', end = '')
          
    def print_red_text_with_blue_bg(self, print_text):
        self.set_cmd_color(self.FOREGROUND_RED | self.FOREGROUND_INTENSITY | self.BACKGROUND_BLUE | self.BACKGROUND_INTENSITY)
        print(print_text, end = '')
        self.reset_color()

def cprint(s, c = None):
    """
    A print() like function, but can make output colorful.

    Usage: [/string to be output, color/], i.e. your string must surrounded by [//]
    An example:
        cprint("[/something red, red/]")
        this would print "something red" in red color.

    This function uses regular express to split input string into 3 parts:
        mc.group(1): text before []
        mc.group(2): text in []
        mc.group(3): text after []

    The function would print mc.group(1) directly,
    print mc.group(2) in specified color,
    then process mc.group(3) iteratively.
    """

    # print(defs.global_encoding)
    if type(s) == type(u""): # if type is unicode
        s = s.encode(defs.global_encoding)

    if not s:
        print('') # print nothing to make a new line
        return

    if not c:
        c = ColorPrint()

    # mc.group(1): text before []
    # mc.group(2): text in []
    # mc.group(3): text after []
    # old pattern [string, color]:   (.*?)(\[.*?\])(.*)
    # -->
    # new pattern [/string, color/]: (.*?)(\[\/.*?\/\])(.*)
    mc = re.search('(.*?)(\[\/.*?\/\])(.*)', s, re.DOTALL)

    # no control parameter, print normally
    if not mc:
        print(s)

    # else color print
    else:
        # deal with text before []
        print(mc.group(1), end = '')

        # deal with text in []
        command = mc.group(2)[2:-2] # strip '[/' and '/]'

        to_p  = command.split(',')[0] # raw string to be print

        # try to get color, if there is no ',' in command, set color as None
        try:
            color = command.split(',')[1].replace(' ', '') # remove spaces in parameter
        except:
            color = None

        if color == 'red':
            c.print_red_text(to_p)

        elif color == 'green':
            c.print_green_text(to_p)

        elif color == 'blue':
            c.print_blue_text(to_p)

        else:
            print(to_p, end = '')

        # deal with text after []
        cprint(mc.group(3), c)

def convert_time(ori_time):
    """
    Convert receiving time to readable format

    ori_time example:
      "Fri Aug 28 00:00:00 +0800 2009"
    """

    week  = ori_time[:3]
    month = ori_time[4:7]
    day   = ori_time[8:10]
    time  = ori_time[11:19]
    year  = ori_time[26:30]

    # something like -> 15:51:54 | Nov 16 2014
    return "{0} | {1} {2} {3}".format(time, month, day, year)

def make_time_numeric(ori_time):
    """
    Convert time from string to int.

    ori_time example:
      "Fri Aug 28 00:00:00 +0800 2009"
    """

    month_to_int = {
        "Jan": "01",  "Feb": "02",
        "Mar": "03",  "Apr": "04",
        "May": "05",  "Jun": "06",
        "Jul": "07",  "Aug": "08",
        "Sep": "09",  "Oct": "10",
        "Nov": "11",  "Dec": "12",
    }

    month = month_to_int[ori_time[4:7]] # "Jan" -> "01"
    day   = ori_time[8:10]
    time  = ori_time[11:19].replace(':', '') # "11:02:06" -> "110206"
    year  = ori_time[26:30]

    # something like: "20150114110206"
    time_str = year + month + day + time

    # something like: 20150114110206
    time_int = int(time_str)

    # return a int time
    return time_int

if __name__ == '__main__':
    cprint("[/[doge], red/]")

    try:
        input()
    except:
        pass


