# -*- coding: utf-8 -*-
"""
create on 2017-12-12 下午6:02

author @heyao
"""


class Config(object):
    @classmethod
    def get(cls, attr_name, default=None):
        return getattr(cls, attr_name, default)


class DevelopmentConfig(Config):
    LOG_LEVEL = 'DEBUG'
    REDIS_URI = 'redis://localhost:6379/3'
    MONGO_URI = 'mongodb://localhost:27017'
    MONGO_DB_NAME = 'haima_spider'
    MONGO_AUTH = {}

    FILE_PATH = '/Users/heyao/haima_spider_txt'


class ProductionConfig(Config):
    LOG_LEVEL = 'INFO'
    REDIS_URI = 'redis://localhost:6379/3'
    MONGO_URI = 'mongodb://localhost:27107'
    MONGO_DB_NAME = 'haima_spider'
    MONGO_AUTH = {}

    FILE_PATH = ''


class TestConfig(Config):
    pass

