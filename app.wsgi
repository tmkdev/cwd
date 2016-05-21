import os
import sys

"""Use this to wrap the app for a WSGI server. Tested in apache"""

sys.path.insert(0, "/home/ubuntu/cwd")
os.chdir(os.path.dirname(__file__))

from cwd import *
application = app
