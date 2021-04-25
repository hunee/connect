#print('__FILE__: ', __file__)

import typing

import os
import yaml

from pathlib import Path

from starlette.config import Config


class Config(Config):
    def _read_file(self, file_name: typing.Union[str, Path]) -> typing.Dict[str, str]:
        file_values = {}  # type: typing.Dict[str, str]
        if os.path.exists(file_name):
            with open(file_name, encoding='utf-8') as f:
                file_values = yaml.load(f, Loader=yaml.FullLoader)
        return file_values

