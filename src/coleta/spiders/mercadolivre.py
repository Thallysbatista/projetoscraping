import scrapy

class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    page_count = 1
    max_pages = 10

    def parse(self, response):
        products = response.css('div.ui-search-result__content')

        for i in products:

            prices = i.css('span.andes-money-amount__fraction::text').getall() 
            cents = i.css('span.andes-money-amount__cents::text').getall() 

            yield {
                'brand': i.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(), 
                'name': i.css('h2.ui-search-item__title::text').get(),
                'old_price': prices[0] if len(prices) > 0 else None,
                'old_price_centavos': cents[0] if len(cents) > 0 else None,
                'new_price': prices[1] if len(prices) > 1 else None,
                'new_price_centavos': cents[1] if len(cents) > 1 else None,
                'reviews_rating_number': i.css('span.ui-search-reviews__rating-number::text').get(),
                'reviews_amount': i.css('span.ui-search-reviews__amount::text').get()
            }

        if self.page_count < self.max_pages: 
            next_page = response.css('li.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)


             
