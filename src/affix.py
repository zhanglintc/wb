#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Intro:
  A module which contains some small functions.

Author:
  Lane(zhanglintc)
"""

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


