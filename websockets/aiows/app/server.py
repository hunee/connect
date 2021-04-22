print('__FILE__: ', __file__)

import asyncio
import json
import logging
import traceback
import sys

###
import websockets

###
from . import handler
from .conn import conn

from .exceptions import AuthException

###
try:
    import signal
except ImportError:
    signal = None


###
from .api import main
###

@asyncio.coroutine
def run_server(ws, path):
    #print('websocket: ', str(ws))

    args_ = {'type':'type', 'msg':'fn', 'text':'b'}
    name_ = 'main.send_fn'
    type_ = 'fn';
    id_ = 'iid';

    payload = json.dumps(dict(type=type_, name=name_, id=id_, args=args_))
    print("> ", payload)

    c = conn(ws)
    #yield from c.send("welcome", c.uid)
    while not c.dead:
        msg = yield from ws.recv()
        if msg is None:
            break

        #logging.debug("< " + str(msg))

        try:
            obj = json.loads(msg)
        except ValueError:
            break

        if not("type" in obj and "name" in obj and "args" in obj):
            break

        type = obj["type"]
        #print('type: ', type)

        try:
            if type == "ev":
                yield from handler.handle_event(c, obj)
            if type == "fn":
                yield from handler.handle_function(c, obj)
        except AuthException:
            yield from c.send("unauthorized")
        except Exception as e:
            logging.warning(e)
            yield from c.send("exception", obj, str(type(e).__name__), str(e))

    yield from c.close()


@asyncio.coroutine
def run(args):
    print('>> def: ' + run.__name__)

    """
    c = conn()

    args1 = {'type':'a', 'text':'b'}
    msg1 = {'name':'main.send', 'args':args1 }

    args2 = {'type':'__a', 'text':'__b', 'msg': '__msg'}
    msg2 = {'name':'main.send_fn', 'args':args2, 'id':'__id' }

    #yield from handle_event(c, msg1)
    yield from handler.handle_function(c, msg2)
    """


def main(args):
    print('Query ws://' + args.host + ':' + str(args.port))

    loop = asyncio.get_event_loop()
    print('Using backend: {0}'.format(loop.__class__.__name__))

    if signal is not None and sys.platform != 'win32':
        loop.add_signal_handler(signal.SIGINT, loop.stop)

    ###
    try:
        start_server = websockets.serve(run_server, args.host, args.port)
        loop.run_until_complete(start_server)

        #loop.run_until_complete(run())

        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
