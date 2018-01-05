# -*- coding: utf-8 -*-
"""
create on 2017-11-24 上午11:42

author @heyao
"""

from content_market.parser.qidian import Qidian
from content_market.parser.shangshu import Shangshu
from content_market.parser.hongxiu import Hongxiu
from content_market.parser.xxsy import Xxsy
from content_market.parser.lieshu import Lieshu
from content_market.parser.biquge import Biquge

qidian = Qidian(__name__, 'DEBUG')
shangshu = Shangshu(__name__, 'DEBUG')
hongxiu = Hongxiu(__name__, 'DEBUG')
xxsy = Xxsy(__name__, 'DEBUG')
lieshu = Lieshu(__name__, 'DEBUG')
biquge = Biquge(__name__, 'DEBUG')


parser_dict = dict(
    Qidian=qidian,
    Shangshu=shangshu,
    Hongxiu=hongxiu,
    Xxsy=xxsy,
    Lieshu=lieshu,
    Biquge=biquge
)


def parse(html, url, parser, parse_func):
    parser = parser_dict.get(parser, None)
    if not parser:
        return None
    if not hasattr(parser, parse_func):
        raise RuntimeError("%s object has no attribute %s" % (parser, parse_func))
    parse_func = getattr(parser, parse_func)
    return parse_func(html, url)
