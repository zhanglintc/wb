# -*- coding: utf-8 -*-
#/usr/bin/env python

"""
Original name: http_helper.py
http_helper.py -> http.py, only because looks better

Refer to:
http://www.cnblogs.com/wly923/archive/2013/04/28/3048700.html

There is also a GitHub project provide thing like this:
http://www.cnblogs.com/wly923/archive/2013/04/28/3048700.html

And its blog:
http://wtm-mac.iteye.com/blog/1623074
"""

import urllib2,cookielib

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(cls, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(cls, req, fp, code, msg, headers)
        result.status = code
        # print headers # commented by zhanglin 2014.11.07
        return result

    def http_error_302(cls, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(cls, req, fp, code, msg, headers)
        result.status = code
        # print headers # commented by zhanglin 2014.11.07
        return result

def get_cookie():
    cookies = cookielib.CookieJar()
    return urllib2.HTTPCookieProcessor(cookies)

def get_opener(proxy = False):
    rv = urllib2.build_opener(get_cookie(), SmartRedirectHandler())
    rv.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')]
    return rv


