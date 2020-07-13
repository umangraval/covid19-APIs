#!/usr/bin/python
import fileinput
import os

try:
    with fileinput.FileInput('./env/lib/python3.8/site-packages/firebase/__init__.py', inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace('.async', '.assync'), end='')

    with fileinput.FileInput('./env/lib/python3.8/site-packages/firebase/firebase.py', inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace('.async', '.assync'), end='')

    os.rename('./env/lib/python3.8/site-packages/firebase/async.py', './env/lib/python3.8/site-packages/firebase/assync.py')
except:
    print('Already Fixed')
