# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/1/4 10:51
    @subject: www.biquge5200.com
"""
from urlparse import urljoin

from lxml import etree

from content_market.parser.base_parser import BaseParser
from content_market.parser.items import BookInfoItem, ChapterListItem


class Biquge(BaseParser):
    def __init__(self, log_name=None, log_level='INFO', format_str=None, filename=None):
        super(Biquge, self).__init__(log_name, log_level, format_str, filename)

    def parse_source_list(self, content, url):
        pass

    def parse_detail(self, content, url):
        item = BookInfoItem()
        if u'不存在的网页' in content:
            return item
        sel = etree.HTML(content)
        item['folder_url'] = urljoin(url, sel.xpath('//div[@id="fmimg"]/img/@src')[0])
        item['title'] = sel.xpath('//div[@id="info"]/h1/text()')[0]
        item['url'] = url
        item['word_count'] = 0
        item['author'] = sel.xpath('//div[@id="info"]/p/text()')[0][7:]
        item['category'] = sel.xpath('//div[@class="con_top"]/a/text()')[1]
        item['sub_category'] = ''
        item['status'] = sel.xpath('//meta[@property="og:novel:status"]/@content')[0]
        item['introduction'] = self.cleaner.fit_transform('\n'.join(sel.xpath('//div[@id="intro"]/p/text()')))
        return item

    def parse_chapter_list(self, content, url):
        try:
            sel = etree.HTML(content)
        except ValueError:
            raise ValueError("can't parse any volume")
        chapters = sel.xpath('//div[@id="list"]/dl/dd')[9:]
        self.logger.debug(chapters)
        chapter_ordinal = 1
        for chapter in chapters:
            item = ChapterListItem()
            try:
                item['title'] = chapter.xpath('./a/text()')[0]
                item['url'] = chapter.xpath('./a/@href')[0]
                item['updated_at'] = ''
                item['word_count'] = 0
                item['chapter_ordinal'] = chapter_ordinal
                chapter_ordinal += 1
                yield item
            except Exception as e:
                self.logger.error(e)

    def parse_content(self, content, url=None):
        sel = etree.HTML(content)
        return self.cleaner.fit_transform('\n'.join(sel.xpath('//div[@id="content"]/text()')))
