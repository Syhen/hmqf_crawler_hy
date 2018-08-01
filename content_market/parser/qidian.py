# -*- coding: utf-8 -*-
"""
create on 2017-11-27 上午10:21

author @heyao
"""

from urlparse import urljoin

from lxml import etree

from content_market.parser.base_parser import BaseParser
from content_market.parser.items import BookSourceItem, BookInfoItem, ChapterListItem


# BaseParser = __import__('hmqf_crawler.parser.data_parser.base_parser.BaseParser')


class Qidian(BaseParser):
    def __init__(self, log_name=None, log_level="INFO", format_str=None, filename=None):
        super(Qidian, self).__init__(log_name, log_level, format_str, filename)

    def parse_source_list(self, content, url):
        sel = etree.HTML(content)
        book_list = sel.xpath('//ul[@class="all-img-list cf"]/li')
        for book in book_list:
            yield self.parse_one(book, url)

    def parse_detail(self, content, url):
        self.logger.debug('Received info')
        item = BookInfoItem()
        if '抱歉，页面无法访问...' in content:
            return item
        sel = etree.HTML(content)
        item['folder_url'] = urljoin(url, sel.xpath('//div[@class="book-information cf"]/div[1]/a/img/@src')[0]).strip()
        item['title'] = sel.xpath('//div[@class="book-information cf"]/div[2]/h1/em/text()')[0]
        item['url'] = url
        # word_count = sel.xpath('//div[@class="book-information cf"]/div[@class="book-info "]/p[3]/em[1]/text()')[0]
        # site = sel.xpath('//div[@class="book-information cf"]/div[@class="book-info "]/p[3]/cite[1]/text()')[0]
        item['word_count'] = 0  #int(self.transform_word_count(word_count, site))
        item['author'] = sel.xpath('//div[@class="book-information cf"]/div[2]/h1/span/a/text()')[0]
        item['category'] = sel.xpath('//div[@class="book-information cf"]/div[2]/p[1]/a[1]/text()')[0]
        item['sub_category'] = sel.xpath('//div[@class="book-information cf"]/div[2]/p[1]/a[2]/text()')[0]
        item['status'] = sel.xpath('//div[@class="book-information cf"]/div[2]/p[1]/span[1]/text()')[0]
        item['introduction'] = self.cleaner.fit_transform('\n'.join(sel.xpath('//div[@class="book-intro"]/p/text()')))
        return item

    def parse_chapter_list(self, content, url):
        try:
            sel = etree.HTML(content)
        except ValueError:
            raise ValueError("can't parse any volume")
        volume_list = sel.xpath(u'//div[@class="volume" and not(contains(., "作品相关"))]')
        chapter_ordinal = 1
        for volume in volume_list:
            if not volume.xpath('./h3/span[@class="free"]'):
                break
            chapters = volume.xpath('./ul/li')
            for chapter in chapters:
                try:
                    item = self._parse_one_chapter(chapter, url)
                    item['chapter_ordinal'] = chapter_ordinal
                    chapter_ordinal += 1
                    yield item
                except Exception as e:
                    self.logger.error(e)

    def _parse_one_chapter(self, element, url):
        item = ChapterListItem()
        item['title'] = element.xpath('./a/text()')[0]
        item['url'] = urljoin(url, element.xpath('./a/@href')[0])
        update_str = element.xpath('./a/@title')[0]
        item['updated_at'] = update_str.rsplit(' ', 1)[0].split(u'：')[-1]
        item['word_count'] = int(update_str.rsplit(' ', 1)[-1].split(u'：')[-1])
        return item

    def parse_content(self, content, url=None):
        sel = etree.HTML(content)
        return self.cleaner.fit_transform('\n'.join(sel.xpath('//div[@class="read-content j_readContent"]/p/text()')))

    def parse_one(self, element, url):
        item = BookSourceItem()
        item['folder_url'] = urljoin(url, element.xpath('./div[1]/a/img/@src')[0]).strip()
        item['title'] = element.xpath('./div[2]/h4/a/text()')[0]
        item['url'] = urljoin(url, element.xpath('./div[2]/h4/a/@href')[0])
        item['author'] = element.xpath('./div[2]/p[1]/a[1]/text()')[0]
        item['category'] = element.xpath('./div[2]/p[1]/a[2]/text()')[0]
        item['sub_category'] = element.xpath('./div[2]/p[1]/a[3]/text()')[0]
        item['status'] = element.xpath('./div[2]/p[1]/span/text()')[0]
        item['introduction'] = self.cleaner.fit_transform(element.xpath('./div[2]/p[2]/text()')[0])
        return item
