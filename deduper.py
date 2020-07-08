"""
Author: Adam Rich
Date:   June 13, 2020
Description:
  Figure out how to create a database of md5 hashes
  on all the files in a given directory.
"""

import sys
import hashlib
import os
# import sqlite3
import socket
if os.name == 'nt':
    import win32api
    import win32con


# Find the home directory of this .py script
pypath = os.path.abspath(__file__)
pydir = os.path.dirname(pypath)
hostname = socket.gethostname()
dbpath = os.path.join(pydir, 'deduper.sqlite')
# dbconn = sqlite3.connect(dbpath)
# dbcurs = dbconn.cursor()


# Pass in a directory path
indir = sys.argv[1]


# Check to make sure it is a directory
if not os.path.isdir(indir):
    sys.exit("ERROR: '" + indir + "' is not a directory.")


# See https://www.tutorialspoint.com/How-to-ignore-hidden-files-using-os-listdir-in-Python
def file_is_hidden(fpath):
    """OS-independent check if a file is hidden"""
    if os.name == 'nt':
        attribute = win32api.GetFileAttributes(fpath)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    return fpath.startswith('.')


# See https://www.pythoncentral.io/hashing-files-with-python/
def hashfile(fpath):
    """Take a file path and return its md5 hexdigest"""
    if not os.path.isfile(fpath):
        return None
    blocksize = 65536
    hasher = hashlib.md5()
    with open(fpath, 'rb') as fhandle:
        buf = fhandle.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = fhandle.read(blocksize)
    return hasher.hexdigest()


# Recursively iterate over the directory to get all files
# https://www.sethserver.com/python/recursively-list-files.html
dirlist = [indir]
while len(dirlist) > 0:
    for (dirpath, dirnames, filenames) in os.walk(dirlist.pop()):
        for dirname in dirnames:
            if file_is_hidden(os.path.join(dirpath, dirname)):
                dirnames.remove(dirname)
        for filename in filenames:
            filepath = os.path.abspath(os.path.join(dirpath, filename))
            if not file_is_hidden(filepath):
                print(filepath + '\t' + hashfile(filepath))
        dirlist.extend(dirnames)
        


# dbconn.close()
