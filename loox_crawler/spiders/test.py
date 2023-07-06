import scrapy
import csv
from scrapy.exporters import CsvItemExporter

class MySpider(scrapy.Spider):
    name = 'my_spider'

    def start_requests(self):
        # Đọc tệp CSV chứa các URL
        with open('dataset/urls.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = row['url']
                yield scrapy.Request(url=url, callback=self.parse, meta={'url': url})

    def parse(self, response):
        # Xử lý dữ liệu thu thập từ trang web
        # Lưu trữ dữ liệu vào tệp CSV riêng
        url = response.meta['url']
        title = response.css('title::text').get()
        a = 'sss'
        b='ccccc'
        # Lưu dữ liệu vào file CSV
        filename = url.split('/')[-1] + '.csv'
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title'])
            writer.writerow([title, a,b])
        # yield data
