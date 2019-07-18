# -*- coding: utf-8 -*-
import scrapy


class UltaSpiderSpider(scrapy.Spider):
    name = 'ulta_spider'
    allowed_domains = ['www.ulta.com']
    start_urls = ['http://www.ulta.com/skin-care?N=2707']

    custom_settings = {'FEED_URI': "output.csv",
                       'FEED_FORMAT': 'csv'}
    '''
    def parse(self, response):
        brands = response.xpath("//h4[@class='prod-title']/a[@href]/text()").extract()
        products = response.xpath("//p[@class='prod-desc']/a[@href]/text()").extract()
        prices = response.xpath("//span[@class='regPrice']/text()").extract()

        row_data = zip(brands,products,prices)

        for item in row_data:
            scraped_info= {
                'brand': item[0].replace('\n','').replace('\t','').replace('\r',''),
                'product': item[1].replace('\n','').replace('\t','').replace('\r',''),
                'price': item[2].replace('\n','').replace('\t','').replace('\r','')
            }
            yield scraped_info
    '''

    def parse(self, response):
        for href in response.xpath("//p[@class='prod-desc']/a/@href").extract():
            url = url='https://www.ulta.com'+href
            #scraped_info={
            #    'url': url
            #}
            #yield scraped_info
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        brand = response.xpath("//div[@class='ProductMainSection__brandName']/a/p[@class]/text()").extract()
        product = response.xpath("//div[@class='ProductMainSection__productName']/span[@class]/text()").extract()
        #size = response.xpath("//div[@class='ProductMainSection__itemNumber']/p[@class]/text()")[0].extract()
        price = response.xpath("//div[@class='ProductPricingPanel']/span[@class]/text()").extract()
        description = response.xpath("//div[@class='ProductDetail__productContent']//text()").extract()
        #purpose = response.xpath("//*[@id='productDetails']/div/ul[1]").extract()
        #benefit = response.xpath("//*[@id='productDetails']/div/ul[2]").extract()
        #ideal_for = response.xpath("//*[@id='productDetails']/div/ul[3]").extract()
        #formula_facts = response.xpath("//*[@id='productDetails']/div/ul[4]").extract()
        how_to_use = response.xpath("//div[@class='ProductDetail__howToUse']/div[2]//text()").extract()
        ingredients = response.xpath("//div[@class='ProductDetail__ingredients']/div[2]/text()").extract()

        row_data = zip(brand, product, price,description,how_to_use,ingredients)

        for item in row_data:
            scraped_info={
                'brand':item[0],
                'product':item[1],
                #'size':item[2],
                'price':item[2],
                'description':item[3].replace(',','.'),
                #'purpose':item[5].replace('<ul>','').replace('<li>','').replace('</li>','').replace('</ul>',''),
                #'benefit':item[6].replace('<ul>','').replace('<li>','').replace('</li>','').replace('</ul>',''),
                #'ideal_for':item[7].replace('<ul>','').replace('<li>','').replace('</li>','').replace('</ul>',''),
                #'formula_facts':item[8].replace('<ul>','').replace('<li>','').replace('</li>','').replace('</ul>',''),
                'how_to_use':item[4],
                'ingredients':item[5]
            }
            yield scraped_info