# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/1/3 11:49
    @subject: 
"""
from content_market.checker.url_parser.utils import parse_url


def parse_hongxiu(url):
    host, path, q = parse_url(url)
    book_id = path.split('/')[2]
    extra_info = {'book_id': book_id, 'url': url}
    return host, path, extra_info
