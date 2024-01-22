import scrapy


class AlphadropsSpider(scrapy.Spider):
    name = 'alphadrops'
    allowed_domains = ['alphadrops.net']
    start_urls = ['http://alphadrops.net/alpha']

    def parse(self, response):
        projects = response.css('div.slate-collection_item._1iqelwt0')

        for project in projects:
            relative_url = project.css('div a::attr(href)').get()
            project_url = 'https://www.alphadrops.net' + relative_url

            yield response.follow(project_url, callback=self.parse_project)

    def parse_project(self, response):
        yield {
            'title': response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[1]/div[1]/div/div/div[2]/h1/span[2]/span/text()').get(),
            'logo': response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/img/@src').get(),
            'tags': response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[1]/div[1]/div/div/div[2]/p/span/span/text()').get(),
            'website': response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[2]/div/div[1]/a/@href').get(),
            'discord': response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[2]/div/div[2]/a/@href').get(),
            'invest': response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[2]/div/div[4]/p[2]/span/span/text()').get(),
            'network': response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[2]/div/div[5]/p[2]/span/span/text()').get(),
            'status': response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[2]/div/div[6]/p[2]/span/span/text()').get(),
            'description': response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[1]/div[2]/p[1]/span/span/text()').get(),
            'strategy': response.xpath('//*[@id="__next"]/div/div[3]/div/div/div[1]/div[2]/p[2]/span/span/text()').get()
        }

