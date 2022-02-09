import scrapy


class QuotesSpider(scrapy.Spider):
    name = "cppsite"

    # Modify this token if you want to scrape different categories
    token = "protein"

    def start_requests(self):
        url = 'https://webs.iiitd.edu.in/raghava/cppsite/browse_sub1.php?token=%s&col=6' % self.token
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for row in response.css("tr"):
            id = row.css("td:nth-of-type(1) a::text").get()
            if id is not None:
                yield {
                    'id': id,
                    'sequence': row.css("td:nth-of-type(2) a::text").get(),
                    'name': row.css("td:nth-of-type(3) font::text").get(),
                    'length': row.css("td:nth-of-type(4) font::text").get(),
                    'chirality': row.css("td:nth-of-type(5) font::text").get(),
                    'linear/cyclic': row.css("td:nth-of-type(6) font::text").get(),
                    'source': row.css("td:nth-of-type(7) font::text").get(),
                    'category': row.css("td:nth-of-type(8) font::text").get(),
                    'N_TERMINAL_MODIFICATION': row.css("td:nth-of-type(9) font::text").get(),
                    'C_TERMINAL_MODIFICATION': row.css("td:nth-of-type(10) font::text").get(),
                    'CHEMICAL_MODIFICATION': row.css("td:nth-of-type(11) font::text").get(),
                    'cargo': row.css("td:nth-of-type(12) font::text").get(),
                    'pubmedid': row.css("td:nth-of-type(13) a::text").get()
                }

        next_page_url = response.css(".pagination a:last-of-type::attr(href)").get()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
        