# -*- coding: utf8 -*-

import os
from dotenv import load_dotenv

from libs.utils.config import BASEDIR


__all__ = ['Config']


# load environment setting from leopaccino/.env to os environ
load_dotenv(dotenv_path=BASEDIR + '/.env')


if os.environ.get('TORNADO_ENV', 'dev') == 'dev':
    from .config_dev import DevConfig
    Config = DevConfig
else:
    from .config_prod import ProdConfig
    Config = ProdConfig
