import os
import json
import scrapy
from urllib.parse import urlparse
from crawl.items import QuestionItem

page = {"start": 5501, "end": 6500}


crawl_url = "https://superuser.com/questions?tab=newest&pagesize=50"


class Spider(scrapy.Spider):
    name = os.path.splitext(os.path.basename(__file__))[0]
    allowed_domains = [urlparse(crawl_url).hostname]
    start_urls = [
        f"{crawl_url}&page={i}" for i in range(page["start"], page["end"] + 1)
    ]

    def parse(self, response):
        # Request tới từng question dựa vào href
        for question in response.css(".js-post-summary"):
            question_url = question.css(
                "div.s-post-summary--content > h3 > a ::attr(href)"
            ).extract_first()
            if question_url.startswith("/questions"):
                item = QuestionItem()

                item["views"] = question.css(
                    ".js-post-summary-stats > div:nth-child(3) > span.s-post-summary--stats-item-number ::text"
                ).extract_first()

                item["num_answer"] = question.css(
                    ".js-post-summary-stats > div:nth-child(2) > span.s-post-summary--stats-item-number ::text"
                ).extract_first()

                item["votes"] = question.css(
                    ".js-post-summary-stats > div.s-post-summary--stats-item.s-post-summary--stats-item__emphasized > span.s-post-summary--stats-item-number ::text"
                ).extract_first()

                item["solved"] = (
                    question.css(
                        ".js-post-summary-stats > div.s-post-summary--stats-item.has-accepted-answer"
                    ).get()
                    is not None
                )

                yield scrapy.Request(
                    response.urljoin(question_url),
                    callback=self.parse_data,
                    cb_kwargs={"item": dict(item)},  # Convert QuestionItem to dict
                )

    def parse_data(self, response, item):
        item["title"] = response.css("#question-header > h1 > a ::text").extract_first()

        item["content"] = response.css(
            "#question > div.post-layout > div.postcell.post-layout--right > div.s-prose.js-post-body"
        ).extract_first()

        item["time"] = response.css(
            "#content > div > div.inner-content.clearfix > div.d-flex.fw-wrap.pb8.mb16.bb.bc-black-200 > div:nth-child(1) > time ::attr(datetime)"
        ).extract_first()

        item["category"] = response.css(
            "#question > div.post-layout > div.postcell.post-layout--right > div.mt24.mb12 > div > div > ul > li > a ::text"
        ).extract()

        # Lưu dữ liệu vào một tệp JSON
        output_filename = self.get_output_filename()
        with open(output_filename, "a") as json_file:
            json.dump(item, json_file)
            json_file.write(",\n")

        yield item

    def get_output_filename(self):
        spider_name = getattr(self, "name", "default")
        spider_dir = "data"
        os.makedirs(spider_dir, exist_ok=True)
        return os.path.join(
            spider_dir, f"{spider_name}-{page['start']}-{page['end']}.json"
        )
