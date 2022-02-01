import scrapy


class QuotesSpider(scrapy.Spider):
    name = "cppsite"

    tab1 = [1,2]

    def start_requests(self):
        for i in self.tab1:
            url = 'https://webs.iiitd.edu.in/raghava/cppsite/browse_sub1.php?token=Linear&col=5&page=%d' % i
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for row in response.css("tr"):
            yield {
                'id': row.css("td:nth-of-type(1) a::text").extract_first(),
                'sequence': row.css("td:nth-of-type(2) a::text").extract_first(),
                'pubmedid': row.css("td:nth-of-type(13) a::text").extract_first()
            }

        next_page_url = response.css(".pagination a:last-of-type::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
        