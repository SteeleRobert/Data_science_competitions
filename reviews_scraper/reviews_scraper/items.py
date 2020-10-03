# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewsScraperItem(scrapy.Item):
    # define the fields for your item here like:
    movieid = scrapy.Field()
    userid = scrapy.Field()
    rating = scrapy.Field()
    date = scrapy.Field()
    text = scrapy.Field() 
