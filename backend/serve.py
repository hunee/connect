#!/usr/bin/python3
import sys
print('=================')
for i, value in enumerate(sys.argv):
    print(('argv[%d]: %s ') % (i, value))