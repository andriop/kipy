'''
    find_xxx.py -- Find the place in the tree where xxx lives.

    Ways to use:
                1) Make a copy, change 'xxx' in package to be your name; or
                2) Under Linux, just ln -s to where this is in the right tree

    Created by Pat Maupin, who doesn't consider it big enough to be worth copyrighting
'''

import sys
import os

myname = __name__[5:]   # remove 'find_'

def trypath(startpath):
    parts = os.path.abspath(startpath).rsplit(myname, 2)
    return len(parts) == 3 and parts[0] or None

root = trypath(__file__) or trypath(os.path.realpath(__file__))

if root is None:
    raise SystemExit('%s: Could not find path to package %s' % (__file__, myname))

if root not in sys.path:
    sys.path.append(root)
