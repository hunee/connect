#print('__FILE__: ', __file__)

import asyncio

import logging
import sys


###
import message


from app import api
from app import models

from app.models import user


###
logger = logging.getLogger(__name__)

class server(message.post):
    def __init__(self, debug: bool = False) -> None:
        logger.info('$$$ ---------- START SERVER ----------')
        
        super().__init__(debug)

        asyncio.ensure_future(user.connect())
        asyncio.ensure_future(models.battle_connect())

def main():
    app = server(debug=True)
    return app

app = main()
