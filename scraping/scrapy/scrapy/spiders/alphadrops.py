import scrapy
from scrapy_playwright.page import PageMethod
from ..items import ScrapingItem

class AlphadropsSpider(scrapy.Spider):
    name = 'alphadrops'

    def start_requests(self):
        yield scrapy.Request(
            url="http://alphadrops.net/alpha",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod('wait_for_selector', 'div._1wmk2026'),
                    PageMethod('click', 'div._1wmk2026'),
                    PageMethod('wait_for_selector', 'div.slate-collection_item._1iqelwt0'),
                ],
                errback=self.errback
            )
        )

    async def parse(self, response):
        page = response.meta['playwright_page']
        await page.close()

        projects = response.css('div.slate-collection_item._1iqelwt0')
        for project in projects:
            relative_url = project.css('div a::attr(href)').get()
            project_url = 'https://www.alphadrops.net' + relative_url

            yield response.follow(project_url, callback=self.parse_project)

    def parse_project(self, response):
        item = ScrapingItem()

        item['title'] = response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[1]/div[1]/div/div/div[2]/h1/span[2]/span/text()').get(),
        item['tags'] = response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[1]/div[1]/div/div/div[2]/p/span/span/text()').get(),
        item['invest'] = response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[2]/div/div[4]/p[2]/span/span/text()').get(),
        item['network'] = response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[2]/div/div[5]/p[2]/span/span/text()').get(),
        item['status'] = response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[2]/div/div[6]/p[2]/span/span/text()').get(),
        item['description'] = response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[1]/div[2]/p[1]/span/span/text()').get(),
        item['strategy'] = response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[1]/div[2]/p[2]/span/span/text()').get()
        item['website'] = response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[2]/div/div[1]/a/@href').get(),
        item['discord'] = response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[2]/div/div[2]/a/@href').get(),
        item['logo'] = response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/img/@src').get(),

        yield item

    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()