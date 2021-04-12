#print('__FILE__: ', __file__)

import typing

from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Type,
    Union,
)

from connect.types import (
    ASGIApp,
    Receive,
    Scope,
    Send,
    DecoratedCallable
)

import logging

import os
import pathlib
import yaml

import sys



###
env = {}

class Env():
    def __init__(self):
        #
        APPLICATION_PATH = os.getcwd()#str(pathlib.Path(__file__).parent.parent)
        #print('->> APPLICATION_PATH: ' + APPLICATION_PATH)

        APPLICATION_DIR = os.path.dirname(os.path.abspath(__file__)) #os.path.dirname(os.path.realpath(__file__))
        #print('->> APPLICATION_DIR: ' + APPLICATION_DIR)


        ###
        PRODUCTION = 'production'
        STAGING = 'staging'
        DEVELOPMENT = 'development'

        ###
        APPLICATION_ENV = os.environ.get('APPLICATION_ENV', DEVELOPMENT)

        ###
        env['APPLICATION_ENV'] = APPLICATION_ENV
        env['APPLICATION_PATH'] = APPLICATION_PATH
        
        ###
        ENV_PATH = '{0}/env/{1}.yaml'.format(APPLICATION_PATH, APPLICATION_ENV)

        if os.path.exists(ENV_PATH):
            with open(ENV_PATH, encoding='utf-8') as f:
                env_dict = yaml.load(f, Loader=yaml.FullLoader)
                env['mysql'] = env_dict['mysql']

        ###
        DOCKER = os.environ.get('DOCKER', "False")
        if 'True' in DOCKER:
            env['mysql']['host'] = 'db'

        mysql = env['mysql']
        env['DATABASE_URL'] = 'mysql+aiomysql://{0}:{1}@{2}:{3}'.format(mysql['user'], mysql['password'], mysql['host'], mysql['port'])


