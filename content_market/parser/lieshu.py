# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2017/01/05 09:41
    @subject: http://www.lieshu.cc
"""
import sys

from content_market.parser.shangshu import Shangshu

reload(sys)
sys.setdefaultencoding('utf-8')


class Lieshu(Shangshu):
    """
    猎书网解析结构和上书网完全一致，so 继承 Shangshu
    """

    def __init__(self, log_name=None, log_level="INFO", format_str=None, filename=None):
        super(Lieshu, self).__init__(log_name, log_level, format_str, filename)
