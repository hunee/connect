#print('__FILE__: ', __file__)

import asyncio

import logging
import sys


###
import connect


from app import api
from app import models

from app.models import user


###
logger = logging.getLogger(__name__)

class server(connect.Connect):
    def __init__(self, debug: bool = False) -> None:
        logger.info('$$$ ---------- START SERVER ----------')
        
        super().__init__(debug)

        asyncio.ensure_future(user.connect())
        asyncio.ensure_future(models.battle_connect())


papp = server(debug=True)
app = connect.GZipMiddleware(papp)
