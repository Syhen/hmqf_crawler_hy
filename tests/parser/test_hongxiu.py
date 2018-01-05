# -*- coding: utf-8 -*-
"""
    @author: harvey
    @time: 2018/1/3 19:41
    @subject: 测试类
"""

import json

from nose.tools import assert_list_equal, assert_is_instance, assert_dict_equal, assert_equal

from content_market.parser.hongxiu import Hongxiu

from unittest import TestCase

TestCase.maxDiff = None


class TestHongxiu(object):
    def setUp(self):
        self.hongxiu = Hongxiu()

    def tear_down(self):
        pass

    def test_chapter_list(self):
        with open('parser/data/hongxiu/book_detail.html', 'r') as f:
            content = f.read().decode('utf-8')
        with open('parser/data/hongxiu/chapters.json', 'r') as f:
            real_chapters = json.load(f)
        url = 'https://www.hongxiu.com'
        chapters = self.hongxiu.parse_chapter_list(content, url)
        assert_is_instance(chapters, type((i for i in (1,))))
        assert_list_equal(list(chapters), real_chapters)

    def test_chapter_content(self):
        with open('parser/data/hongxiu/chapter_content.html', 'r') as f:
            content_page = f.read().decode('utf-8')
        with open('parser/data/hongxiu/chapter_content.txt', 'r') as f:
            content = f.read().decode('utf-8')
        assert_equal(content, self.hongxiu.parse_content(content_page))

    def test_book_detail(self):
        with open('parser/data/hongxiu/book_detail.html', 'r') as f:
            content = f.read().decode('utf-8')
        with open('parser/data/hongxiu/book_detail.json', 'r') as f:
            book_detail = json.load(f)
        url = 'https://www.hongxiu.com/book/6972481904230701'
        info = self.hongxiu.parse_detail(content, url)
        assert_dict_equal(book_detail, dict(info))
