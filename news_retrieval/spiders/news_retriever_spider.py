import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'news'

    start_urls = ['http://www.dailynews.lk/date/2015-10-01']

    def parse(self, response):
        # follow links to news pages
        for href in response.css('.views-field.views-field-title span.field-content a::attr(href)'):
            yield response.follow(href, self.parse_news_page)

        # follow pagination links
        for href in response.css('li.date-next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_news_page(self, response):
        def extract_with_css(query):
            return response.css(query).extract()

        yield {
             'heading': extract_with_css('#page.clearfix div#main-content div.container div.row section.col-md-8 div#main.clearfix h1#page-title.title::text'),
             'posted_date': extract_with_css('span.date-display-single::text'),
             'category': extract_with_css('div.field.field-name-field-section.field-type-taxonomy-term-reference.field-label-hidden div.field-items div.field-item.even a::text'),
             'author': extract_with_css('div.field.field-name-field-author-byline.field-type-taxonomy-term-reference.field-label-hidden div.field-items div.field-item.even a::text'),
             'text': extract_with_css('div.content div.field.field-name-body.field-type-text-with-summary.field-label-hidden div.field-items div.field-item.even p::text'),
             #  'count_agree': extract_with_css('div.item-list ul li.first::text'),
             # 'count_disagree': extract_with_css('div.item-list ul li.second::text'),
             # 'count_neutral': extract_with_css('#rate-button-3::text'),
             # 'count_clueless': extract_with_css('#rate-button-4::text'),
             # 'count_not_relevent': extract_with_css('#rate-button-5::text'),
             # 'count_sad': extract_with_css('#rate-button-6::text'),
        }