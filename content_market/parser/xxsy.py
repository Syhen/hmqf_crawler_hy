# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/1/2 14:59
    @subject: www.xxsy.net
"""
from urlparse import urljoin

from lxml import etree

from content_market.parser.base_parser import BaseParser
from content_market.parser.items import BookInfoItem, ChapterListItem


class Xxsy(BaseParser):
    def __init__(self, log_name=None, log_level="INFO", format_str=None, filename=None):
        super(Xxsy, self).__init__(log_name, log_level, format_str, filename)

    def parse_detail(self, content, url):
        self.logger.debug('Received info')
        item = BookInfoItem()
        if u'找不到页面' in content:
            return item
        sel = etree.HTML(content)
        item['folder_url'] = urljoin(url, sel.xpath('//dl[@class="bookprofile"]/dt/img/@src')[0])
        item['title'] = sel.xpath('//div[@class="title"]/h1/text()')[0]
        item['url'] = url
        item['author'] = sel.xpath('//div[@class="title"]/span/a/text()')[0]
        item['category'] = sel.xpath('//p[@class="sub-cols"]/span/text()')[2].strip().split(u'：')[-1]
        item['sub_category'] = ''
        word_count = sel.xpath('//p[@class="sub-data"]/span/em/text()')[0][:-1]
        site = sel.xpath('//p[@class="sub-data"]/span/em/text()')[0]
        item['word_count'] = int(self.transform_word_count(word_count, site))
        item['status'] = sel.xpath('//p[@class="sub-cols"]/span/text()')[1]
        item['introduction'] = self.cleaner.fit_transform(
            '\n'.join(sel.xpath('//dl[@class="introcontent"]/dd/p/text()')))
        return item

    def parse_chapter_list(self, content, url):
        try:
            sel = etree.HTML(content)
        except ValueError:
            raise ValueError("can't parse any volume")
        chapters = sel.xpath('//ul[@class="catalog-list cl"]/li')
        chapter_ordinal = 1
        for chapter in chapters:
            if chapter.xpath('./i[@class="iconfont"]'):
                break
            item = ChapterListItem()
            try:
                item['title'] = chapter.xpath('./a/text()')[0]
                item['url'] = urljoin(url, chapter.xpath('./a/@href')[0])
                item['updated_at'] = ''
                item['word_count'] = 0
                item['chapter_ordinal'] = chapter_ordinal
                chapter_ordinal += 1
                yield item
            except Exception as e:
                self.logger.error(e)

    def parse_content(self, content, url=None):
        sel = etree.HTML(content)
        return self.cleaner.fit_transform('\n'.join(sel.xpath('//div[@class="chapter-main"]/p/text()')))

    def parse_source_list(self, content, url):
        pass
