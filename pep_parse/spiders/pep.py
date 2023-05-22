import scrapy

from ..items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        for pep_link in response.css(
            '#numerical-index tbody tr a::attr(href)'
        ).getall():
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response, **kwargs):
        headline_parts = response.css(
            'h1.page-title::text'
        ).get().split(' – ')
        yield PepParseItem({
            'number': headline_parts[0].split()[1],
            'name': headline_parts[1],
            'status': response.css(
                'dt:contains("Status") + dd abbr::text'
            ).get(),
        })
