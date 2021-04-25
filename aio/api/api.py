from .app_env import env
from pprint import pprint

import asyncio
import logging

import traceback
import sys

import json

import sqlalchemy as sa

print('__FILE__: ', __file__)

def _a():
    print('>> func: ', _a.__name__)
    return _a.__name__

def _b():
    print('>> func: ', _b.__name__)
    return _b.__name__

def _c():
    print('>> func: ', _c.__name__)
    return _c.__name__

switch_n = { 1: _a, 2: _b }
switch_str = { '1': _a, '2': _b }



meta = sa.MetaData()

사용자_정보 = sa.Table('사용자_정보', meta,
                    sa.Column('사용자_id', sa.Integer, nullable=False),
                    sa.Column('비밀번호', sa.String(200), nullable=False),
                    sa.Column('등록_날짜', sa.Date, nullable=False),
                    sa.PrimaryKeyConstraint('사용자_id', name='사용자_id_pkey'))


event_handlers = dict()
function_handlers = dict()

def handler(fn):
    """
    Register a function to receive and handle events.
    """
    module = fn.__module__.split(".")[-1]
    key = module + "." + fn.__name__
    logging.info("registering event handler: '" + key + "' from " + fn.__module__)
    fn = asyncio.coroutine(fn)
    event_handlers[key] = fn
    return fn


def function(fn):
    """
    Register a function to receive a request and return a result
    """
    module = fn.__module__.split(".")[-1]
    key = module + "." + fn.__name__
    logging.info("registering function handler: '" + key + "' from " + fn.__module__)
    fn = asyncio.coroutine(fn)
    function_handlers[key] = fn
    return fn

@asyncio.coroutine
def handle_function(conn, msg):
    #print('>> def: ' + handle_function.__name__)

    name = msg["name"]
    args = msg["args"]
    id = msg['id']

    #print('name: ', name)
    #print('args: ', args)

    try:
        result = yield from function_handlers[name](conn, *args)
        #print('result: ', str(result))

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        yield from conn.send("return", name, id, False, str(type(e).__name__ + " " + str(e)))
    else:
        yield from conn.send("return", name, id, True, result)

@asyncio.coroutine
def handle_event(conn, msg):
    #print('>> def: ' + handle_event.__name__)

    name = msg["name"]
    args = msg["args"]
    #print('name: ', name)
    #print('args: ', args)

    try:
        yield from event_handlers[name](conn, *args)
        #event_handlers[name](c, **args)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)


@handler
def send(c, type, text):
    #print('>> def: ' + send.__name__)

    #print('>> def: ', send.__name__)
    #print('c:',c, ' type:', type, ' text:', text)
    pass


@function
def send_fn(c, type, text, msg):
    #print('>> def: ' + send_fn.__name__)

    #print('>> def: ', send_fn.__name__)
    #print('c:',c, ' type:', type, ' text:', text, ' msg:', msg)

    return {'result': 'OK'}

@asyncio.coroutine
def app_main():
    #print('>> def: ', app_main.__name__)


    """
    n = 1
    switch_n[n]()

    str = '2'
    switch_str[str]()


    a = 3
    # Get the function from switcher dictionary
    func = switch_n.get(a, lambda: "nothing")
    print('r: ', func())

    print('APPLICATION_PATH: ', env['APPLICATION_PATH'])
    print('APPLICATION_ENV: ', env['APPLICATION_ENV'])
    """

    """
    print('DATABASE_USER:')
    pprint(env['DATABASE_USER'])
    """

    """
    pconn = {}

    def get_사용자_DATABASE(사용자_id):
        print('>> def: ', get_사용자_DATABASE.__name__)
        for v in env['DATABASE_USER']:
            if 사용자_id >= v['range'][0] and 사용자_id <= v['range'][1]:
                return env['DATABASE_USER'].index(v)

        else:
            return -1

    사용자_id = 101
    index = get_사용자_DATABASE(사용자_id)

    print('사용자_id: ', 사용자_id, ', index: ', index)


    query = 사용자_정보.select()
    print('query: ', query)

    """

    class conn():
        #yield from conn.send("return", name, id, True, result)
        @asyncio.coroutine
        def send(self, msg, *args):
            print('>> def: ' + type(self).__name__ + '.' + type(self).send.__name__)

            print('msg: ', msg)
            print('*args: ', args)

            yield from self._send("ev", msg, args)

        @asyncio.coroutine
        def _send(self, type_, msg, args):
            print('>> def: ' + type(self).__name__ + '.' + type(self)._send.__name__)

            print('msg: ', msg)
            print('args: ', args)

            payload = json.dumps(dict(type=type_, msg=msg, args=args))
            print("> ", payload)

            #try:
            #    yield from self.ws.send(payload)
            #except websockets.exceptions.InvalidState:
            #    yield from self.close()



    c = conn()

    args1 = {'type':'a', 'text':'b'}
    msg1 = {'name':'api.send', 'args':args1 }

    args2 = {'type':'__a', 'text':'__b', 'msg': '__msg'}
    msg2 = {'name':'api.send_fn', 'args':args2, 'id':'__id' }

    #yield from handle_event(c, msg1)
    yield from handle_function(c, msg2)


def main():

    try:
        asyncio.get_event_loop().run_until_complete(app_main())
        #asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
