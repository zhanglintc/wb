#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lane's Weibo Client Application Beta, Nothing Reserved
"""

from weibo import Client
import sys
import webbrowser
import json
import pickle

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


# ACCESS_TOKEN = {u'access_token': u'2.00_ShHyB2HnvNCca83c087d04aFAkC', u'remind_in': u'157679999', u'uid': u'1804547715', u'expires_at': 1569833194}

API_KEY = '2038131539' # app key
API_SECRET = 'b4d84f59af3e5a52c8df1f0e7ccfa75d' # app secret
REDIRECT_URI = 'http://zhanglintc.blog.163.com' # callback url

def update_access_token():
    """
    Get ACCESS_TOKEN form file 'token'. It will direct you to weibo.com to get
    a new ACCESS_TOKEN if failed to find the file 'token'.

    Try to delete file 'token' so that you can get a new one if this application
    not running correctly.
    """

    try:
        fr = open('token', 'rb')
        ACCESS_TOKEN = pickle.load(fr)
        fr.close()

    except IOError:
        c = Client(API_KEY, API_SECRET, REDIRECT_URI)
        webbrowser.open(c.authorize_url)

        code = input('Paste code here:\n')
        c.set_code(code)

        fw = open('token', 'wb')
        pickle.dump(c.token, fw)
        fw.close()

        ACCESS_TOKEN = c.token

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
    print('All the comments have downloaded')


def get_friends_timeline(client):
    """Show 20 friends_timeline in the screen"""

    received = client.get('statuses/friends_timeline')
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
        print('Successfully updated!')

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

if __name__ == "__main__":
    ACCESS_TOKEN = update_access_token()

    client = Client(API_KEY, API_SECRET, REDIRECT_URI, ACCESS_TOKEN)
    get_friends_timeline(client)
    # get_comments_to_me(client, 1, 5)
    # post_statuses_update(client, 'From Xiao霸王其乐无穷')
    # post_statuses_upload(client, 'From Xiao霸王其乐无穷', r'picture_path_here')




