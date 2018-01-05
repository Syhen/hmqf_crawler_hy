# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/1/4 14:27
    @subject: http://www.biquge5200.com
"""
from content_market.checker.url_parser.utils import parse_url


def parse_biquge(url):
    host, path, q = parse_url(url)
    book_id = path.split('/')[1].split('_')[1]
    extra_info = {'book_id': book_id, 'url': url}
    return host, path, extra_info
