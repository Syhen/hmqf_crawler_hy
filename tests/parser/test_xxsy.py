# -*- coding: utf-8 -*-
"""
create on 2017-11-27 上午11:15

author @heyao
"""

import json

from nose.tools import assert_list_equal, assert_is_instance, assert_dict_equal, assert_equal

from content_market.parser.xxsy import Xxsy


class TestXxsy(object):
    def setUp(self):
        self.xxsy = Xxsy()

    def tear_down(self):
        pass

    def test_chapter_list(self):
        with open('parser/data/xxsy/chapters.html', 'r') as f:
            content = f.read().decode('utf-8')
        with open('parser/data/xxsy/chapters.json', 'r') as f:
            real_chapters = json.load(f)
        url = 'http://www.xxsy.net/'
        chapters = self.xxsy.parse_chapter_list(content, url)
        assert_is_instance(chapters, type((i for i in (1,))))
        assert_list_equal(list(chapters), real_chapters)

    def test_chapter_content(self):
        with open('parser/data/xxsy/chapter_content.html', 'r') as f:
            content_page = f.read().decode('utf-8')
        with open('parser/data/xxsy/chapter_content.txt', 'r') as f:
            content = f.read().decode('utf-8')
        assert_equal(content, self.xxsy.parse_content(content_page))

    def test_book_detail(self):
        with open('parser/data/xxsy/book_detail.html', 'r') as f:
            content = f.read().decode('utf-8')
        with open('parser/data/xxsy/book_detail.json', 'r') as f:
            book_detail = json.load(f)
        url = 'http://www.xxsy.net/info/897569.html'
        info = self.xxsy.parse_detail(content, url)
        assert_dict_equal(book_detail, dict(info))
