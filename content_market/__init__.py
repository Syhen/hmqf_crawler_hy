# -*- coding: utf-8 -*-
"""
create on 2017-11-24 上午11:39

author @heyao
"""

import os

from content_market.settings import DevelopmentConfig, TestConfig
from content_market.production_settings import ProductionConfig

config = dict(
    default=DevelopmentConfig,
    development=DevelopmentConfig,
    production=ProductionConfig,
    testing=TestConfig
)
config_name = os.environ.get("TOOLS_CONFIG_NAME", 'default')
config = config[config_name]
