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

from .types import (
    ASGIApp,
    Receive,
    Scope,
    Send,
    DecoratedCallable,
)

import logging
import logging.config
import logging.handlers

import os
import pathlib
import yaml

import sys

from .config import config

class Logger():
    def __init__(self):
        pass
    
        # 로그 저장할 폴더 생성
        LOG_PATH = '{}/logs'.format(env['APPLICATION_PATH'])
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)

        print('->> LOG_PATH: ' + LOG_PATH)


        ###
        LOGGING_CONFIG_PATH = '{}/config/logging.yaml'.format(env['APPLICATION_PATH'])
        print('->> LOGGING_CONFIG_PATH: ' + LOGGING_CONFIG_PATH)

        if os.path.exists(LOGGING_CONFIG_PATH):
            with open(LOGGING_CONFIG_PATH, encoding='utf-8') as f:
                logging.config.dictConfig(yaml.load(f, Loader=yaml.FullLoader))

