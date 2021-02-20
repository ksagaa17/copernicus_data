import scrapy
class WholePageSpider(scrapy.Spider):
    name = "Paige"

    start_urls = [
        "",
    ]

    def parse(self, response):
        filename = response.url.split("/")[-1] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

