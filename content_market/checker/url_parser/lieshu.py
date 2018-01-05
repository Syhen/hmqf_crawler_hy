# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2017/01/05 09:57
    @subject: 
"""
from content_market.checker.url_parser.utils import parse_url


def parse_lieshu(url):
    host, path, q = parse_url(url)
    book_id = path.split('/')[-2]
    extra_info = {'book_id': book_id, 'url': url}
    return host, path, extra_info
