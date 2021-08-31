# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scarpy.exporters import CsvItemExporter


class ReviewsScraperPipeline:
	def __init__(self):
		self.reviews = open('C:/Users/steel/Dropbox/DataCompetitions/west_coast_datacomp/test.csv', 'wb') 
		self.exporter = CsvItemExporter(self.reviews, unicode)
        self.exporter.start_exporting()


	def close_spider(self, spider):
		self.reviews.close()


    def process_item(self, item, spider):
    	self.exporter.export_item(item)
    	return item





