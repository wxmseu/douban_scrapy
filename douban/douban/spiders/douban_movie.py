import scrapy
from scrapy import Selector, Request
from ..items import MovieItem
import re

class DoubanMovieSpider(scrapy.Spider):
    name = "douban_movie"
    allowed_domains = ["movie.douban.com"]

    # start_urls = ["https://movie.douban.com/top250"]
    def start_requests(self):
        # 考虑到爬取速度和封账号ip的风险，可将此处设置只爬取第一页的信息
        # for page in range(1):
        for page in range(10):
            url = f'https://movie.douban.com/top250?start={page * 25}&filter='
            yield Request(url=url)

    def parse(self, response, **kwargs):
        sel = Selector(response)
        list_items = sel.css('#content > div > div.article > ol > li')
        for list_item in list_items:
            url_detail = list_item.css('div.info > div.hd > a::attr(href)').get()
            movie_item = MovieItem()
            movie_item['title'] = list_item.css('span.title::text').get()
            movie_item['rank'] = list_item.css('span.rating_num::text').get()
            movie_item['descript'] = list_item.css('span.inq::text').get()
            yield Request(
                url=url_detail,
                callback=self.parse_detail,
                cb_kwargs={'movie_item': movie_item},
            )

    def parse_detail(self, response, **kwargs):
        movie_item = kwargs['movie_item']
        sel = Selector(response)
        movie_item['duration'] = sel.css(
            'span[property="v:runtime"]::attr(content)'
        ).extract_first()
        text=sel.css('span[property="v:summary"]::text').extract_first() or ''
        movie_item['comments'] = (re.sub('\s','',text))
        yield movie_item
