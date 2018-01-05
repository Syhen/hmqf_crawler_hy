# -*- coding: utf-8 -*-
"""
    @author: harvey
    @time: 2018/1/4 16:51
    @subject: 测试类
"""

import json

from nose.tools import assert_list_equal, assert_is_instance, assert_dict_equal, assert_equal

from content_market.parser.biquge import Biquge


class TestBiquge(object):
    def setUp(self):
        self.biquge = Biquge()

    def tear_down(self):
        pass

    def test_chapter_list(self):
        with open('parser/data/biquge/book_detail.html', 'r') as f:
            content = f.read().decode('utf-8')
        with open('parser/data/biquge/chapters.json', 'r') as f:
            real_chapters = json.load(f)
        url = 'http://www.biquge5200.com'
        chapters = self.biquge.parse_chapter_list(content, url)
        assert_is_instance(chapters, type((i for i in (1,))))
        assert_list_equal(list(chapters), real_chapters)

    def test_chapter_content(self):
        with open('parser/data/biquge/chapter_content.html', 'r') as f:
            content_page = f.read().decode('utf-8')
        with open('parser/data/biquge/chapter_content.txt', 'r') as f:
            content = f.read().decode('utf-8')
        assert_equal(content, self.biquge.parse_content(content_page))

    def test_book_detail(self):
        with open('parser/data/biquge/book_detail.html', 'r') as f:
            content = f.read().decode('utf-8')
        with open('parser/data/biquge/book_detail.json', 'r') as f:
            book_detail = json.load(f)
        url = 'http://www.biquge5200.com/86_86306/'
        info = self.biquge.parse_detail(content, url)
        assert_dict_equal(book_detail, dict(info))
