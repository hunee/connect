__version__ = '0.0.1'

#print('__FILE__: ', __file__)
#print('__VERSION__: ', __version__)

"""@package docstring
Documentation for this module.
 
More details.
"""

###
from .applications import Server
from .config import Config

from .routing import post, websocket
from .message import Message

from .functools import function, function_async, profile, Singleton


#Logger()