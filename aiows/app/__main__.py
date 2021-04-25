print('__FILE__: ', __file__)

import argparse

import asyncio
import json
import logging
import traceback
import sys

###
logging.basicConfig(level=logging.DEBUG)
###

from . import server

###
ARGS = argparse.ArgumentParser(description="Run websocket server.")
ARGS.add_argument(
        '--host', action="store", dest='host',
        default='127.0.0.1', help='Host name')
ARGS.add_argument(
        '--port', action="store", dest='port',
        default=8765, type=int, help='Port number')
ARGS.add_argument(
        '--workers', action="store", dest='workers',
        default=2, type=int, help='Number of workers.')


"""
"""
if __name__ == '__main__':

    ###
    args = ARGS.parse_args()
    if ':' in args.host:
        args.host, port = args.host.split(':', 1)
        args.port = int(port)

    ###
    server.main(args)
