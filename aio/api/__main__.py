import pathlib


import json
import yaml

from pprint import pprint

from . import api

from .app_env import env


print('__FILE__: ', __file__)


"""
"""
if __name__ == '__main__':



    ###
    APPLICATION_PATH = str(pathlib.Path(__file__).parent.parent)

    ###
    PRODUCTION = 'production'
    STAGING = 'staging'

    APPLICATION_ENV = PRODUCTION

    ###
    if PRODUCTION in APPLICATION_PATH:
        print(APPLICATION_ENV, 'production')
    else:
        print(APPLICATION_ENV, 'staging')


    env['APPLICATION_PATH'] = APPLICATION_PATH
    env['APPLICATION_ENV'] = PRODUCTION

    #print('APPLICATION_PATH: ', env['APPLICATION_PATH'])
    #print('APPLICATION_ENV: ', env['APPLICATION_ENV'])


    """
    path = str(APPLICATION_PATH + '/config/' + APPLICATION_ENV + '.json')
    with open(path, encoding='utf-8') as file:
        data = json.loads(file.read())
        pprint(data)
    """


    """
    """
    path = str(APPLICATION_PATH + '/config/' + APPLICATION_ENV + '.yaml')
    with open(path, encoding='utf-8') as file:
        data = yaml.load(file.read())
        #pprint(data)

        env['DATABASE_MASTER'] = data['DATABASE']['MASTER']
        env['DATABASE_USER'] = data['DATABASE']['USER']
        env['DATABASE_BATTLE'] = data['DATABASE']['BATTLE']

        env['HOST'] = data['HOST']
        env['PORT'] = data['PORT']


    """
    """
    api.main()
