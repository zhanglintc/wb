#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Name:
  Power_wb, a command-line tool for Weibo.

Version:
  beta, nothing reserved

Author:
  Lane(zhanglintc)

Description:
  Based on "lxyu/weibo", work on Python 2.x.x, support Linux/Mac/Windows.
  Support automatic installation by using "python setup.py".
  More details visit: https://github.com/zhanglintc/wb

"""

from http import *
from affix import *
from sdk import Client
# import tkFileDialog # comment by zhanglin 2014.11.12
import sys, os
import pickle
import getpass
import argparse
import urllib, urllib2
import configparser
import platform
import sqlite3
import webbrowser

# get version & set encoding
version = sys.version[0]
input = raw_input if version == '2' else input
reload(sys)
sys.setdefaultencoding('utf8')

# get OS information
plat = platform.platform()
if 'Linux' in plat:
    plat = 'Lin'
elif 'Darwin' in plat:
    plat = 'Mac'
elif 'Windows' in plat:
    plat = 'Win'
else:
    plat = None

# set path
TOKEN_PATH  = sys.path[0] + '/token'
CONFIG_PATH = sys.path[0] + '/config.ini'

# read config.ini
config = configparser.ConfigParser()
config.read(CONFIG_PATH)
API_KEY      = config['Weibo']['API_KEY']
API_SECRET   = config['Weibo']['API_SECRET']
REDIRECT_URI = config['Weibo']['REDIRECT_URI']

##########################################################################
# Functions are defined below
##########################################################################
def open_weibo_or_target(client, number):
    """
    Try to open a target URL by using default browser.
    If target URL is specifically set, open it,
    otherwise open weibo.com directly.

    API refer to: http://open.weibo.com/wiki/2/statuses/querymid
    """

    NULL, id, cid = database_handler("query", number = number)
    recv = client.get('statuses/querymid', id = id, type = 1)
    print recv.mid

    # if number == 'weibo.com':
    #     webbrowser.open_new_tab('http://weibo.com')

    # else:
    #     pass

def database_handler(handle_type, data = None, number = None):
    """
    Database management function.

    Database design:
        | number int | id int | cid int |

    parameters:
        handle_type:
            insert:  insert data to database
            query:   get data from database
            clean:   clean entire table

        data:
            a list of input data.

            data[0]: number
            data[1]: id
            data[2]: cid

        number:
            displaying number of weibos, use to get a specific weibo id & cid

    return:
        a list of output data.

        ret[0]: number
        ret[1]: id
        ret[2]: cid
    """

    # prepare for using database
    conn = sqlite3.connect(sys.path[0] + "/data.db")
    c = conn.cursor()

    try:
        c.execute('create table weibo(number int, id int, cid int)')

    except sqlite3.OperationalError:
        pass

    # main process
    if handle_type is 'insert':
        # clean table before use
        c.execute("delete from weibo")

        for item in data:
            c.execute('insert into weibo values (?, ?, ?)', item)

        ret = None

    elif handle_type is 'query':
        ret = c.execute('select * from weibo where number={}'.format(number)).fetchone() # may be unsafe, see Python sqlite3 help file

    elif handle_type is 'clean':
        c.execute("delete from weibo")
        ret = None

    else:
        pass

    # finish use database
    conn.commit()
    conn.close()

    # return
    return ret

def log_in_to_weibo():
    """
    Log in to weibo and get the ACCESS_TOKEN.
    If success, store it to 'token' file,
    if not, do nothing.
    """

    print('')
    print("please enter your username and password below\n")

    client = Client(API_KEY, API_SECRET, REDIRECT_URI)

    USERID = input("username: ")
    USERPASSWD = getpass.getpass("password: ") # getpass() makes password invisible

    print('')
    print('logging...')
    code = make_access_token(client, USERID, USERPASSWD)
    if not code: # while log in failed
        print('') # a blank line to make better look
        print("bad username or password, please try again!\n")

    # after got code, store it
    else:
        client.set_code(code)
        fw = open(TOKEN_PATH, 'wb')
        pickle.dump(client.token, fw)
        fw.close()
        print('')
        print("log in to weibo.com successfully\n")

def log_out_from_weibo():
    """delete login informations"""

    os.remove(TOKEN_PATH)

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
        fr = open(TOKEN_PATH, 'rb')
        ACCESS_TOKEN = pickle.load(fr)
        fr.close()

    except IOError:
        ACCESS_TOKEN = None

    return ACCESS_TOKEN

def comments_to_me_To_File(client, start_page, end_page):
    """
    Download comments from 'start_page' to 'end_page'

    API refer to:
    http://open.weibo.com/wiki/2/comments/to_me

    Deprecated, merely use => by zhanglin 2014.11.21
    """

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

def get_comments_to_me(client, count):
    """
    Get comments to me and display in screen.

    API refer to:
    http://open.weibo.com/wiki/2/comments/to_me
    http://open.weibo.com/wiki/2/comments/mentions

    Display example:
    No.1: (to_me)
    11:53:00 | Jan 10 2015 | from @左手心的寂寞在北京:
    回复@Lane麟:不应该这么设计吧
    """

    if int(count) > 200:
        print("error: cannot get comments more than 200\n")
        return

    os.system('cls') if plat == 'Win' else os.system('clear')
    print('') # a blank line makes better look
    print("getting latest {} comments to me...\n".format(count))

    # get comments to me & add type
    received_to_me = client.get('comments/to_me', count = count)
    for item in received_to_me.comments:
        item['type'] = 'to_me'

    # get comments mentioned me & add type
    received_mentions = client.get('comments/mentions', count = count)
    for item in received_mentions.comments:
        item['type'] = 'mentions'

    to_be_saved = []

    # combine comments to me & comments mention
    comments_all = received_to_me.comments + received_mentions.comments
    # [ lambda x, y: cmp(y, x) ] makes new -> old (descending, bigger -> smaller)
    # [ lambda x, y: cmp(x, y) ] makes old -> new (ascending, smaller -> bigger)
    # here is new -> old
    comments_all = sorted(comments_all, cmp = lambda x, y: cmp(make_time_numeric(y.created_at), make_time_numeric(x.created_at)))

    index = int(count)
    for item in comments_all[int(count) - 1::-1]: # [from:to:-1] makes old -> new
        to_be_saved.append([index, item.status.id, item.id]) # cache ids and cids

        print\
            ('No.{0}: ({1})\n{2} | from @{3}:\n{4}\n'.format
                (
                    index, # 0
                    item.type, # 1
                    convert_time(item.created_at), # 2
                    item.user.name, # 3
                    item.text, # 4
                )
            ).encode('utf8')
        index -= 1

    # save data to database
    database_handler('insert', data = to_be_saved)

def get_friends_timeline(client, count):
    """
    Show friends_timeline in the screen

    API refer to:
    http://open.weibo.com/wiki/2/statuses/friends_timeline

    Display example:
    1. Without retweet:
        No.1:
        11:12:42 | Jan 11 2015 | by @王尼玛:
        王尼玛教你学数学

    2. With retweet:
        No.1:
        12:32:07 | Jan 11 2015 | by @王尼玛:
        看着大家都在@邓超 我也来一发，超哥赶紧来学数学了！
        =========================================================
        11:12:42 | Jan 11 2015 | by @王尼玛:
        王尼玛教你学数学
        =========================================================
    """

    if int(count) > 100:
        print("error: cannot get weibos more than 100\n")
        return

    os.system('cls') if plat == 'Win' else os.system('clear')
    print('') # a blank line makes better look
    print("getting latest %s friend's weibo...\n") % count

    received = client.get('statuses/friends_timeline', count = count)
    to_be_saved = []

    index = int(count) # used in No.{index} below
    for item in received.statuses[::-1]: # from old to new
        retweet = item.get('retweeted_status') # if this is retweet or not

        to_be_saved.append([index, item.id, None])

        # print normal content first
        print\
            ('No.{}:\n{} | by @{}:\n{}'.format
                (
                    str(index),
                    convert_time(item.created_at),
                    item.user.name,
                    item.text,
                ).encode('utf8')
            )

        # if this is not retweet, just print a blank line
        if not retweet:
            print('')

        # if this is retweet, print the retweeted content
        else:
            print('=========================================================')

            # if original Weibo has been deleted, only print text
            if 'deleted' in item.retweeted_status:
                print((item.retweeted_status.text).encode('utf8'))

            # else print normally
            else:
                print\
                ('{} | by @{}:\n{}'.format
                    (
                        convert_time(item.retweeted_status.created_at),
                        item.retweeted_status.user.name,
                        item.retweeted_status.text,
                    ).encode('utf8')
                )

            print('=========================================================\n')

        index -= 1

    database_handler('insert', data = to_be_saved)

def show_status(client):
    """
    Show unread informations.

    API refer to:
    http://open.weibo.com/wiki/2/remind/unread_count
    """

    print('') # a blank line makes better look
    print("getting status...\n")

    received = client.get('remind/unread_count')

    print("unread weibo    => {}".format(received.status))
    print("new comments    => {}".format(received.cmt))
    print("new mentions    => {}".format(received.mention_status + received.mention_cmt))
    print("direct messages => {}".format(received.dm))
    print('') # blank line makes better look

def post_statuses_update(client, text):
    """ 
    Update a new weibo(text only) to Sina

    API refer to:
    http://open.weibo.com/wiki/2/statuses/update
    """

    print('')
    print('sending...\n')

    try:
        client.post('statuses/update', status = text)
        print('=========================================================')
        print(text)
        print('=========================================================')
        print('has been successfully posted!\n')

    except RuntimeError as e:
        print("sorry, send failed because: {}\n".format(str(e)))

def post_statuses_upload(client, text):
    """
    Upload a new weibo(with picture) to Sina
    Currently not in use from 2014.11.12
    Maybe reuse in the future

    API refer to:
    http://open.weibo.com/wiki/2/statuses/upload
    """

    # 2014.11.12 zhanglin make it useless -S
    picture = tkFileDialog.askopenfilename() # get picture by GUI
    # 2014.11.12 zhanglin make it useless -E

    print('')
    print('sending...\n')

    try:
        f = open(picture, 'rb')
        client.post('statuses/upload', status = text, pic = f)
        f.close()

        print('=========================================================')
        print(text + '\n(with picture)')
        print('=========================================================')
        print('has been successfully posted!\n')

    except (RuntimeError, IOError) as e:
        print("sorry, send failed because: {}\n".format(str(e)))

def post_comment_reply(client, number, comment):
    """
    function:
        Make a reply. If replying to a weibo, set cid as None.

    parameters:
        number: number of weibo or comment wish to reply

    API refer to:
    http://open.weibo.com/wiki/2/comments/create
    http://open.weibo.com/wiki/2/comments/reply
    """

    print("replying...")

    # IDs[0]:number   IDs[1]:id   IDs[2]:cid
    IDs = database_handler('query', number = int(number))
    id, cid = IDs[1], IDs[2]

    # reply to a comment
    if cid:
        client.post('comments/reply', id = id, cid = cid, comment = comment)

    # reply to a weibo
    else:
        client.post('comments/create', id = id, comment = comment)

    print("succeed!!!")

def creat_parser():
    parser = argparse.ArgumentParser(
        prog = "wb",
        # usage = 'wb -option [option1, option2...]',
        description = "wb -- A command-line tool for Weibo",
        epilog = 'This code is out sourced on Github,\
                    please visit https://github.com/zhanglintc/wb\
                    for further infomations',
        prefix_chars = '-', # remove '/' to solve image sending problem(there is '/' in path)
        fromfile_prefix_chars = '@',
        argument_default = argparse.SUPPRESS,
        )

    parser.add_argument('-authorize', metavar = '-a', nargs = '?', const = 'True', help = "sign in to 'weibo.com'")
    parser.add_argument('-comment', metavar = '-c', nargs = '?', const = 5, help = "get comments to me")
    parser.add_argument('-delete', metavar = '-d', nargs = '?', const = 'True', help = "delete your token infomation") 
    parser.add_argument('-get', metavar = '-g', nargs = '?', const = 5, help = "get latest N friend's timeline")
    # parser.add_argument('-image', metavar = '-i', nargs = 1, help = "post a new weibo with image")
    parser.add_argument('-open', metavar = '-o', nargs = '?', const = 'weibo.com', help = "open weibo.com or a target")
    parser.add_argument('-post', metavar = '-p', nargs = 1, help = "post a new weibo")
    parser.add_argument('-reply', metavar = '', nargs = 2, help = "reply a weibo")
    parser.add_argument('-tweet', metavar = '-t', nargs = 1, help = "post a new weibo(alias of -p)")
    parser.add_argument('common', nargs = '?', help = "status/...")

    return parser

##########################################################################
##########################################################################

if __name__ == "__main__":
    ACCESS_TOKEN = update_access_token()
    client = Client(API_KEY, API_SECRET, REDIRECT_URI, ACCESS_TOKEN)

    parser = creat_parser()
    params = vars(parser.parse_args())
    # print params

    if not params:
        print('')
        print('- Note: type "wb -h/--help" to see usages.\n')

##########################################################################

    # Start of common command
    elif params.get('common') == 'status':
        show_status(client)
    # End of common command

##########################################################################

    # Start of hyphen command
    elif params.get('authorize'):
        log_in_to_weibo()

    elif params.get('delete'):
        log_out_from_weibo()

    elif params.get('get'):
        get_friends_timeline(client, params['get'])

    # comment by zhanglin 2014.11.12 -S
    # elif params.get('image'):
        # post_statuses_upload(client, params['image'][0])
    # comment by zhanglin 2014.11.12 -E

    elif params.get('open'):
        open_weibo_or_target(client, params.get('open'))

    elif params.get('reply'):
        post_comment_reply(client, params['reply'][0], params['reply'][1])

    elif params.get('post'):
        post_statuses_update(client, params['post'][0])

    elif params.get('tweet'):
        post_statuses_update(client, params['tweet'][0])

    elif params.get('comment'):
        get_comments_to_me(client, params['comment'])
    # End of hyphen command

##########################################################################

    else:
        print('')
        print('- Note: unrecognized command, type "wb -h/--help" to see usages.\n')





