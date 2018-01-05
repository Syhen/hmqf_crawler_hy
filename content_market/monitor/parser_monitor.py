# -*- coding: utf-8 -*-
"""
create on 2017-12-19 下午2:28

author @heyao
"""
import os
from copy import deepcopy
import datetime

from content_market.checker import hosts_config, chapter_config, UrlChecker
from content_market.checker.key_inject import inject
from content_market.monitor.warm import WarmMonitor
from content_market.parser import parse
from content_market.utils.pool import mongo
from content_market.utils.pool import config as global_config
from content_market.utils.save import save_content


class BookDetailMonitor(WarmMonitor):
    def __init__(self, queue, scheduler=None, mongodb=None, *args, **kwargs):
        log_name = self.__class__.__module__ + '.' + self.__class__.__name__
        kwargs.pop('log_name', None)
        kwargs['log_name'] = log_name
        super(BookDetailMonitor, self).__init__(queue, scheduler, *args, **kwargs)
        self.url_checker = UrlChecker(hosts_config, chapter_config)
        self.mongodb = mongodb

    def one_step(self, data):
        html = data['html']
        url = data['url']
        url_type = data['url_type']
        config = data['config']
        extra_info = data['extra']
        parser = config['parser']
        parse_func = config['parse_func']

        detail_info = parse(html, url, parser, parse_func)
        if not detail_info:
            self.mongodb['book_index'].update_one(
                {'_id': '%s_%s' % (extra_info['source'], extra_info['book_id'])},
                {'$set': {'status': 0}}
            )
            self.logger.debug('no info for url: %s' % url)
            return
        detail_info.update(extra_info)
        detail_info['added_at'] = datetime.datetime.now()
        detail_info['finished_status'] = 1
        self.mongodb['book_detail'].update_one(
            {'_id': '%s_%s' % (detail_info['source'], detail_info['book_id'])},
            {'$set': detail_info},
            upsert=True
        )
        detail_info.pop('added_at')
        self.logger.debug('successful parse detail for source %s, book %s\n %s'
                          % (detail_info['source'], detail_info['book_id'], detail_info))
        chapter_request_data, config = self.url_checker.check_chapter_url(url)
        if chapter_request_data:
            chapter_request_data['url_type'] = 'chapter'
            chapter_request_data['config'] = config
            chapter_request_data['extra'] = extra_info
            self.scheduler.schedul(chapter_request_data)
        return True


class BookChapterMonitor(WarmMonitor):
    def __init__(self, queue, scheduler=None, mongodb=None, *args, **kwargs):
        log_name = self.__class__.__module__ + '.' + self.__class__.__name__
        kwargs.pop('log_name', None)
        kwargs['log_name'] = log_name
        super(BookChapterMonitor, self).__init__(queue, scheduler, *args, **kwargs)
        self.mongodb = mongodb

    def one_step(self, data):
        html = data['html']
        url = data['url']
        url_type = data['url_type']
        config = data['config']
        extra_info = data['extra']
        parser = config['parser']
        parse_func = config['parse_func']

        chapter_list = parse(html, url, parser, parse_func)
        for chapter in chapter_list:
            chapter['source'] = extra_info['source']
            chapter['book_id'] = extra_info['book_id']
            chapter['added_at'] = datetime.datetime.now()
            chapter['finished_status'] = 0
            result = self.mongodb['book_chapter'].update_one(
                {'_id': '%s_%s_%s' % (chapter['source'], chapter['book_id'], chapter['chapter_ordinal'])},
                {'$setOnInsert': chapter},
                upsert=True
            )
            if not result.matched_count:
                self.logger.debug('successful parse chapter for source %s, book %s, chapter %s\n %s'
                                  % (extra_info['source'], extra_info['book_id'], chapter['chapter_ordinal'], chapter))
                chapter.pop('added_at')
                chapter_request_data = data['config']
                self.logger.debug(chapter_request_data)
                chapter_request_data = {k: inject(chapter_request_data[k], **chapter) for k in chapter_request_data}
                if chapter_request_data:
                    chapter_request_data['url_type'] = 'content'
                    chapter_request_data['config'] = config['content_config']
                    chapter_request_data['url'] = chapter_request_data['data_url']
                    extra_info.update(chapter)
                    chapter_request_data['extra'] = extra_info
                    self.scheduler.schedul(chapter_request_data)
            else:
                self.logger.debug('already have book: source %s, book_id %s, chapter_id %s' %
                                  (extra_info['source'], extra_info['book_id'], chapter['chapter_ordinal']))


class BookContentMonitor(WarmMonitor):
    def __init__(self, queue, scheduler=None, mongodb=None, *args, **kwargs):
        log_name = self.__class__.__module__ + '.' + self.__class__.__name__
        kwargs.pop('log_name', None)
        kwargs['log_name'] = log_name
        super(BookContentMonitor, self).__init__(queue, scheduler, *args, **kwargs)
        self.mongodb = mongodb

    def one_step(self, data):
        html = data['html']
        url = data['url']
        url_type = data['url_type']
        config = data['config']
        extra_info = data['extra']
        parser = config['parser']
        parse_func = config['parse_func']

        content = parse(html, url, parser, parse_func)
        save_content(
            os.path.join(global_config.get("FILE_PATH"), str(extra_info['source']), str(extra_info['book_id'])),
            '%s.txt' % extra_info['chapter_ordinal'],
            content
        )
        self.mongodb['book_chapter'].update_one(
            {'_id': '%s_%s_%s' % (extra_info['source'], extra_info['book_id'], extra_info['chapter_ordinal'])},
            {'$set': {'finished_status': 1}},
            upsert=True
        )
        self.logger.debug('successful parse content for source %s, book %s, chapter %s\n %s'
                          % (extra_info['source'], extra_info['book_id'], extra_info['chapter_ordinal'], content))
