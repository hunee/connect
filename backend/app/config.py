__version__ = '0.0.1'

#print('__FILE__: ', __file__)
#print('__VERSION__: ', __version__)

import logging

import os
import pathlib
import sys

from connect import Config

###
logger = logging.getLogger(__name__)


APPLICATION_PATH = os.getcwd()#str(pathlib.Path(__file__).parent.parent)
logger.info('->> APPLICATION_PATH: ' + APPLICATION_PATH)

APPLICATION_DIR = os.path.dirname(os.path.abspath(__file__)) #os.path.dirname(os.path.realpath(__file__))
logger.info('->> APPLICATION_DIR: ' + APPLICATION_DIR)


PRODUCTION = 'production'
STAGING = 'staging'
DEVELOPMENT = 'development'

APPLICATION_ENV = os.environ.get('APPLICATION_ENV', DEVELOPMENT)
logger.info('->> APPLICATION_ENV: ' + APPLICATION_ENV)


###
config = Config('{0}/config/{1}.yaml'.format(APPLICATION_PATH, APPLICATION_ENV))


###
def get_database_url(db):
    host = 'db'
    if 'False' in os.environ.get('DOCKER', "False"):
        host = db['host']

    return 'mysql+aiomysql://{0}:{1}@{2}:{3}/{4}'.format(db['user'], db['password'], host, db['port'], db['database'])


def get_redis_url(db):
    host = 'redis'
    if 'False' in os.environ.get('DOCKER', "False"):
        host = db['host']

    return 'redis://{0}'.format(host)


