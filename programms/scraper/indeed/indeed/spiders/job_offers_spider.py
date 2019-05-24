
# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http.request import Request


class JobOffersSpider(Spider):
    name = 'job_offers_spider'
    allowed_domains = ['de.indeed.com']

    def __init__(self, query="python", location="Berlin", country="de"):
        print("\nQuery : {0}\n".format(query))
        self.query = query
        self.location = location
        self.country = country
        self.start_urls = [
            'https://{2}.indeed.com/jobs?q={0}&l={1}'.format(self.query, self.location, self.country)
        ]

    def parse(self, response):
        # set base url of the indeed website for the country
        if self.country == "fr":
            self.home = "https://www.indeed.{0}".format(self.country)
        else:
            self.home = "https://{0}.indeed.com".format(self.country)

        job_urls = response.xpath(
            "//a[@data-tn-element='jobTitle']/@href").extract()
        for job_url in job_urls:
            job_abs_url = self.home + job_url
            yield Request(job_abs_url, callback=self.parse_job)

        # looks for next pages depending on the country
        next = "Weiter" if self.country == "de" else "Suivant"
        next_page_url = response.xpath(
            "//*[@class='np' and contains(text(), '{0}')]/parent::*/parent::*/@href".format(next)
        )
        if next_page_url is not []:
            next_page_url = next_page_url.extract_first()
            next_page_abs_url = self.home + next_page_url
            print(next_page_abs_url)
            yield Request(next_page_abs_url, callback=self.parse)

    def parse_job(self, response):
        url = response.url

        job_header = response.xpath("//*[contains(@class, 'JobComponent')]")

        title = job_header.xpath(
            "//*[contains(@class, 'title')]/text()").extract_first()
        company = job_header.xpath(
            "./descendant::*[contains(@class, 'Company')]/*[1]/text()").extract_first()
        location = job_header.xpath(
                        "./descendant::*[contains(@class, 'Company')]/*[3]/text()").extract_first()
        if location is "-":
            location = job_header.xpath(
                        "./descendant::*[contains(@class, 'Company')]/*[4]/text()").extract_first()
            
        contract = job_header.xpath(
            "./descendant::*[contains(@class, 'MetadataHeader')]/text()").extract_first()

        desc = response.xpath(
            "(//*[contains(@class, 'description')]|//*[contains(@class, 'summary')])").extract()
        if desc == []:
            desc = response.xpath(
                "(//*[contains(@class, 'description')]|//*[contains(@class, 'summary')])/descendant::*").extract()
            if desc == []:
                desc = response.xpath(
                    "//*[contains(@id, 'job-content')]/descendant::*").extract()

        days_ago = job_header.xpath(
            "./descendant::*[contains(@class, 'jobsearch-JobMetadataFooter')]/text()").extract_first()
        days_ago = days_ago.split(" ")
        for piece in days_ago:
            try:
                days_ago = int(piece[:2])
            except ValueError:
                continue

        print(
            "url", url,
            "title", title,
            "company", company,
            "location", location,
            "contract", contract,
            "desc", desc,
            "days_ago", days_ago,
            "query" , self.query
        )
        
        yield {
            "url": url,
            "title": title,
            "company": company,
            "contract": contract,
            "desc": desc,
            "days_ago": days_ago,
            "query" : self.query,
            "search_location" : self.location,
            "result_location" : location
        }
