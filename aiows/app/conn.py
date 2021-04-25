print('__FILE__: ', __file__)

import asyncio
import json
import logging
import traceback
import sys

import hashlib
import os
import random

###
import websockets


class conn():
    def __init__(self, ws):
        self.ws = ws
        self.uid = hashlib.md5(os.urandom(8)).hexdigest()
        self.authenticated = False
        self.dead = False

    #yield from conn.send("return", name, id, True, result)
    @asyncio.coroutine
    def send(self, msg, **args):
        print('>> def: ' + type(self).__name__ + '.' + type(self).send.__name__)

        #print('msg: ', msg)
        #print('*args: ', args)

        yield from self._send("ev", msg, args)

    @asyncio.coroutine
    def _send(self, type_, msg, args):
        print('>> def: ' + type(self).__name__ + '.' + type(self)._send.__name__)

        #print('msg: ', msg)
        #print('args: ', args)

        payload = json.dumps(dict(type=type_, msg=msg, args=args))
        print("> ", payload)

        try:
            yield from self.ws.send(payload)
        except websockets.exceptions.InvalidState:
            yield from self.close()


    @asyncio.coroutine
    def close(self):
        #self.register.remove(self.member_id)
        #self.dead = True
        #if self.member_id in self.clients:
        #    self.clients.pop(self.member_id)
        #for r in self.rooms:
        #    r.remove(self)
        pass