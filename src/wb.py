#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lane's Weibo Client Application Beta, Nothing Reserved
"""

from http_helper import *
from sdk import Client
import sys, os
import pickle
import getpass
import argparse
import urllib, urllib2
import configparser


version = sys.version[0]

if version == '2':
    # default encoding
    reload(sys)
    sys.setdefaultencoding('utf8')

    # input method
    input = raw_input

elif version == '3':
    #input method
    input = input

else:
    # do nothing
    pass

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY      = config['Weibo']['API_KEY']
API_SECRET   = config['Weibo']['API_SECRET']
REDIRECT_URI = config['Weibo']['REDIRECT_URI']

##########################################################################
# Functions are defined below
##########################################################################
def log_in_to_weibo():
    """
    Log in to weibo and get the ACCESS_TOKEN.
    If success, store it to 'token' file,
    if not, do nothing.
    """

    print "please enter your username and password below\n"

    client = Client(API_KEY, API_SECRET, REDIRECT_URI)

    USERID = input("username: ")
    USERPASSWD = getpass.getpass("password: ") # getpass() makes password invisible

    print('')
    print('logging...')
    code = make_access_token(client, USERID, USERPASSWD)
    if not code: # while log in failed
        print "" # a blank line to make better look
        print "bad username or password, please try again!\n"

    # after got code, store it
    else:
        client.set_code(code)
        fw = open('token', 'wb')
        pickle.dump(client.token, fw)
        fw.close()
        print "log in to weibo.com successfully"

def log_out_from_weibo():
    """delete login informations"""

    os.remove('token')

def make_access_token(client, USERID, USERPASSWD):
    """
    Refer to: http://www.cnblogs.com/wly923/archive/2013/04/28/3048700.html
    This function can automatically get 'code' from redirected URL and return it.
    """

    params = urllib.urlencode({
        'action':'submit',
        'withOfficalFlag':'0',
        'ticket':'',
        'isLoginSina':'',
        'response_type':'code',
        'regCallback':'',
        'redirect_uri':REDIRECT_URI,
        'client_id':API_KEY,
        'state':'',
        'from':'',
        'userId':USERID,
        'passwd':USERPASSWD,
        })

    login_url = 'https://api.weibo.com/oauth2/authorize'

    url = client.authorize_url
    content = urllib2.urlopen(url)

    if content:
        headers = { 'Referer' : url }
        request = urllib2.Request(login_url, params, headers)
        opener = get_opener(False)
        urllib2.install_opener(opener)

        try:
            f = opener.open(request)
            return_redirect_uri = f.url
        except urllib2.HTTPError, e:
            return_redirect_uri = e.geturl()

        if return_redirect_uri == login_url:
            code = False
        else:
            code = return_redirect_uri.split('=')[1]

    else:
        code = False

    return code

def update_access_token():
    """Try to load ACCESS_TOKEN from 'token' file"""

    try:
        fr = open('token', 'rb')
        ACCESS_TOKEN = pickle.load(fr)
        fr.close()

    except IOError:
        ACCESS_TOKEN = None

    return ACCESS_TOKEN

def get_comments_to_me(client, start_page, end_page):
    """Download comments from 'start_page' to 'end_page'"""

    my_page = start_page

    fw = open('comments.txt', 'wb')

    while my_page <= end_page:
        try:
            print('Page {} is downloading'.format(my_page))
            received = client.get('comments/to_me', count = 20, uid = 1804547715, page = my_page)

        except:
            print('Page {} is downloading has failed'.format(my_page))
            continue

        fw.write('\n\nPage {}:\n'.format(my_page).encode('utf8'))
        for item in received.comments:
            to_be_written = '{0}: {1} by {2}\n'.format(item.created_at, item.text, item.user.name)
            fw.write(to_be_written.encode('utf8'))

        fw.flush()
        my_page += 1

    fw.close()
    print('All the comments have been downloaded')


def get_friends_timeline(client, count):
    """Show friends_timeline in the screen, default 10"""

    received = client.get('statuses/friends_timeline', count = count)
    index = 1
    for item in received.statuses:
        retweet = item.get('retweeted_status')

        if retweet: # have original weibo
            print('No.{0}:\n{1} by @{2}\n-- {3} by @{4}\n'.format
            (
                str(index),
                item.text,
                item.user.name,
                item.retweeted_status.text,
                item.retweeted_status.user.name).encode('utf8')
            )

        else: # no original weibo
            print('No.{0}:\n{1} by @{2}\n'.format
            (
                str(index),
                item.text,
                item.user.name).encode('utf8')
            )

        index += 1

def post_statuses_update(client, text):
    """Update a new weibo(text only) to Sina"""

    try:
        client.post('statuses/update', status = text)
        print('your weibo:\n' + ' '.join(text))
        print('successfully updated!')

    except RuntimeError as e:
        print("Failed because: '{}'".format(str(e)))

def post_statuses_upload(client, text, picture):
    """Upload a new weibo(with picture) to Sina"""

    try:
        f = open(picture, 'rb')
        client.post('statuses/upload', status = text, pic = f)
        f.close()

        print('Successfully updated!')

    except (RuntimeError, IOError) as e:
        print("Failed because: '{}'".format(str(e)))

def creat_parser():
    parser = argparse.ArgumentParser(
        prog = "wb",
        usage = 'wb -option [option1, option2...]',
        description = "wb -- A command-line tool for Weibo",
        epilog = 'This code is out sourced on Github,\
                    please visit https://github.com/zhanglintc/wb\
                    for further infomations',
        prefix_chars = '-/',
        fromfile_prefix_chars = '@',
        argument_default = argparse.SUPPRESS,
        )

    parser.add_argument('-authorize', metavar = '-a', nargs = '?', const = 'True', help = "sign in to 'weibo.com'")
    parser.add_argument('-delete', metavar = '-d', nargs = '?', const = 'True', help = "delete your token infomation") 
    parser.add_argument('-get', metavar = '-g', nargs = '?', const = 10, help = "get latest N friend's timeline")
    parser.add_argument('-image', metavar = '-i', nargs = '+', help = "post a new weibo with image")
    parser.add_argument('-post', metavar = '-p', nargs = '+', help = "post a new weibo")
    parser.add_argument('-tweet', metavar = '-t', nargs = '+', help = "post a new weibo(alias of -p)")

    return parser

##########################################################################
##########################################################################

if __name__ == "__main__":
    ACCESS_TOKEN = update_access_token()
    client = Client(API_KEY, API_SECRET, REDIRECT_URI, ACCESS_TOKEN)

    parser = creat_parser()
    parameters = vars(parser.parse_args())
    # print parameters

    if not parameters:
        print ''
        print '- Note: type "wb -h/--help" to see usages.\n'

    elif parameters.get('authorize'):
        log_in_to_weibo()

    elif parameters.get('delete'):
        log_out_from_weibo()

    elif parameters.get('get'):
        get_friends_timeline(client, parameters['get'])

    elif parameters.get('post'):
        post_statuses_update(client, parameters['post'])

    elif parameters.get('tweet'):
        post_statuses_update(client, parameters['tweet'])

    else:
        pass





