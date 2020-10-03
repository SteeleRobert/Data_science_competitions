import scrapy
import re
import pandas as pd 
import csv
from reviews_scraper.items import ReviewsScraperItem
imdb = pd.read_csv('../data/movie_lense/links.csv')
MAX_REVIEWS = 50000
MAX_DEPTH = 2500
    

partician = [0,1,2,3]
total_particians = 16

class review_spider(scrapy.Spider):
    name= 'imdb_review_spider'

    
    start_urls = ['https://www.imdb.com/title/tt00' + str(imdb['imdbId'][i]) + '/reviews?ref_=tt_urv'for i in range(len(imdb)) if i%16 in partician]
    
    def parse(self, response):
        cur_reviews = 0
        global MAX_REVIEWS
        cur_reviews = 0
        for item in response.css('.lister-item-content'):
            yield ReviewsScraperItem(movieid = re.findall('tt\d+', response.url)[0],userid = item.css('.display-name-link ::text').extract()[0], rating = ''.join(item.css('.rating-other-user-rating ::text').extract()[6:8]), date = item.css('.review-date ::text').extract()[0], text = ''.join(item.css('.text ::text').extract()))
            cur_reviews += 1
            if(cur_reviews > MAX_REVIEWS):
                break
        yield response.follow(response.url.split('reviews')[0] + 'reviews/_ajax?ref_=undefined&paginationKey=' + response.css('.load-more-data').attrib['data-key'], callback= self.parse2, cb_kwargs=dict(cur_reviews=cur_reviews, max_depth= 0))

    def parse2(self, response, cur_reviews, max_depth):
        global MAX_DEPTH
        if max_depth < MAX_DEPTH:
            global MAX_REVIEWS
            for item in response.css('.lister-item-content'):
                clean_txt = re.sub(r'[^a-zA-Z0-9_. ]', '', ''.join(item.css('.text ::text').extract()))
                yield ReviewsScraperItem(movieid = re.findall('tt\d+', response.url)[0],userid = item.css('.display-name-link ::text').extract()[0], rating = ''.join(item.css('.rating-other-user-rating ::text').extract()[6:8]), date = item.css('.review-date ::text').extract()[0], text = clean_txt)
                cur_reviews += 1
                print(max_depth)
                if(cur_reviews > MAX_REVIEWS):
                    break
            next_id = response.css('.load-more-data')
            max_depth += 1
            
            if(next_id):
                yield response.follow(response.url.split('reviews')[0] + 'reviews/_ajax?ref_=undefined&paginationKey=' + next_id.attrib['data-key'], callback= self.parse2, cb_kwargs=dict(cur_reviews=cur_reviews, max_depth=max_depth))
        