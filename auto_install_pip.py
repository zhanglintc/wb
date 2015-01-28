# coding=utf-8

import os, sys
import urllib

# down load get-pip.py
def report_hook(count, blockSize, totalSize):
    percent = int(count * blockSize * 100 / totalSize)
    sys.stdout.write("\r%d%%" % percent + ' completed')
    sys.stdout.flush()

url = 'https://raw.github.com/pypa/pip/master/contrib/get-pip.py'
print('download begin, please wait...')

file_path, headers = urllib.urlretrieve(url, reporthook = report_hook)

with open(file_path, "rb") as fr:
    data = fr.read()

with open('./download.py','wb') as fw:
    fw.write(data)

print('')
print('download success, installing...')

# install pip by calling get-pip.py(i.e. download.py)
import download
download.main()


