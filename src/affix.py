#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A module which contains some small functions
"""

def convert_time(ori_time):
    """Convert receiving time to readable format"""

    # ori_time example:
    # "Fri Aug 28 00:00:00 +0800 2009"

    week  = ori_time[:3]
    month = ori_time[4:7]
    day   = ori_time[8:10]
    time  = ori_time[11:19]
    year  = ori_time[26:30]

    # something like -> 15:51:54 | Nov 16 2014
    return "{} | {} {} {}".format(time, month, day, year)


