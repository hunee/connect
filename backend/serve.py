#!/usr/bin/python3

#print('__FILE__: ', __file__)

import argparse

import uvicorn


###
ARGS = argparse.ArgumentParser(description="Run web server.")
ARGS.add_argument(
        '--host', action="store", dest='host',
        default='127.0.0.1', help='Host name')
ARGS.add_argument(
        '--port', action="store", dest='port',
        default=8000, type=int, help='Port number')


###
if __name__ == '__main__':
    args = ARGS.parse_args()
    if ':' in args.host:
        args.host, port = args.host.split(':', 1)
        args.port = int(port)

    uvicorn.run("app.main:app", host=args.host, port=args.port, reload=True, log_config="./logging.yaml")
