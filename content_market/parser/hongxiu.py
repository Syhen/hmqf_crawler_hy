# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/1/3 11:59
    @subject: www.hongxiu.com
"""
from urlparse import urljoin

from lxml import etree

from content_market.parser.base_parser import BaseParser
from content_market.parser.items import BookInfoItem, ChapterListItem


class Hongxiu(BaseParser):
    def __init__(self, log_name=None, log_level='INFO', format_str=None, filename=None):
        super(Hongxiu, self).__init__(log_name, log_level, format_str, filename)

    def parse_source_list(self, content, url):
        pass

    def parse_detail(self, content, url):
        item = BookInfoItem()
        if u'抱歉，页面无法访问...' in content:
            return item
        sel = etree.HTML(content)
        item['folder_url'] = urljoin(url, sel.xpath('//a[@id="bookImg"]/img/@src')[0].replace('\r', ''))
        item['title'] = sel.xpath('//div[@class="book-info"]/h1/em/text()')[0]
        item['url'] = url
        item['author'] = sel.xpath('//div[@class="book-info"]/h1/a/text()')[0][:-2]
        item['category'] = sel.xpath('//div[@class="crumbs-nav center1020"]/span/a/text()')[1]
        item['sub_category'] = sel.xpath('//div[@class="crumbs-nav center1020"]/span/a/text()')[2]
        item['status'] = sel.xpath('//span[@class="tag"]/i[@class="blue"]/text()')[0]
        word_count = sel.xpath('//p[@class="total"]/span/text()')[0]
        site = sel.xpath('//p[@class="total"]/em/text()')[0]
        item['word_count'] = int(self.transform_word_count(word_count, site))
        item['introduction'] = self.cleaner.fit_transform(
            '\n'.join(sel.xpath('//div[@class="book-information cf"]//p[@class="intro"]/text()')))
        return item

    def parse_chapter_list(self, content, url):
        try:
            sel = etree.HTML(content)
        except ValueError:
            raise ValueError("can't parse any volume")
        chapters = sel.xpath('//div[@class="volume"]/ul/li')
        chapter_ordinal = 1
        for chapter in chapters:
            if chapter.xpath('./em[@class="iconfont "]'):
                break
            item = ChapterListItem()
            try:
                item['title'] = chapter.xpath('./a/text()')[0]
                item['url'] = urljoin(url, chapter.xpath('./a/@href')[0])
                update_str = chapter.xpath('./a/@title')[0]
                item['updated_at'] = update_str.split(' ')[0].split('：')[1]
                item['word_count'] = update_str.split(' ')[1].split('：')[1]
                item['chapter_ordinal'] = chapter_ordinal
                chapter_ordinal += 1
                yield item
            except Exception as e:
                self.logger.error(e)

    def parse_content(self, content, url=None):
        sel = etree.HTML(content)
        return self.cleaner.fit_transform('\n'.join(sel.xpath('//div[@class="read-content j_readContent"]/p/text()')))
