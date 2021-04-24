#print('__FILE__: ', __file__)

import logging
import logging.config
import logging.handlers

import os
import pathlib
import sys
import typing
import yaml


class Logger():
    def __init__(self):
        APPLICATION_PATH = os.getcwd()

        # 로그 저장할 폴더 생성
        LOG_PATH = '{}/logs'.format(APPLICATION_PATH)
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)

        print('->> LOG_PATH: ' + LOG_PATH)

        
        LOGGING_CONFIG_PATH = '{}/logging.yaml'.format(APPLICATION_PATH)
        #print('->> LOGGING_CONFIG_PATH: ' + LOGGING_CONFIG_PATH)

        if os.path.exists(LOGGING_CONFIG_PATH):
            with open(LOGGING_CONFIG_PATH, encoding='utf-8') as f:
                logging.config.dictConfig(yaml.load(f, Loader=yaml.FullLoader))
