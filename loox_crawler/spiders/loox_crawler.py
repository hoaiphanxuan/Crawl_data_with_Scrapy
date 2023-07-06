
import scrapy
import datetime
import csv
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
class collect_reviews(scrapy.Spider):
  name='review_crawler' 
  

  def __init__(self, url=None, **kwargs):
    # super().__init__(**kwargs)
    # self.start_urls = url
    self.id = ''

  def start_requests(self):
    # Đọc tệp CSV chứa các URL
    with open('dataset/urls.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row['url']
            yield scrapy.Request(url=url, callback=self.parse, meta={'url': url})


    
  def parse(self, response):
    # lấy id
    txt =  response.xpath('//*[@id="__st"]/text()').get()
    pid = txt.split('\"rid\"')[1]
    pid = pid[1:-2]
    self.id= pid 
    
    # tạo url trang review
    url_review = 'https://loox.io/widget/VJWWjdB8-a/reviews/' + pid 
    if pid:
      yield scrapy.Request(url=url_review, callback=self.parse1, meta={'pid': pid, 'url': response.meta['url']})


  def parse1(self, response):
    # lấy id
    pid = response.meta['pid']

    #lấy số lượng comment
    number_rev = response.xpath('//*[@id="header"]/div[1]/div[1]/div[2]/span/text()').get()


    if number_rev:
        number_rev = number_rev.split()[0]
        
        # tạo url trang review
        # url_review = 'https://loox.io/widget/VJWWjdB8-a/reviews/' + pid +'?limit=' + number_rev
        url_product_id = response.meta['url']
        url_product_id = url_product_id.replace("abera.us", "store.abera.us")
        yield scrapy.Request(url=url_product_id, callback=self.parse2, meta={'pid': pid, 'numb' : number_rev})

  def parse2(self, response):
    if response.status == 200:
      # lấy id
      pid = response.meta['pid']

      #lấy số lượng comment
      number_rev = response.meta['numb']

      #product_id
      product_id = response.css('#comment_post_ID::attr(value)').get()

      # tạo url trang review
      url_review = 'https://loox.io/widget/VJWWjdB8-a/reviews/' + pid +'?limit=' + number_rev
      yield scrapy.Request(url=url_review, callback=self.parse3, meta={'pid': pid, 'product_id': product_id})
    


  def parse3(self, response):
    # lấy id
    pid = response.meta['pid']

    reviews = response.xpath('//*[@id="grid"]/*')
    
    filename = 'dataset/' + pid + '.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['review_content', 'review_score', 'date', 'product_id', 'display_name','email','order_id','media'])

    for rev in reviews:
        image_link = ''
        type_review = rev.xpath('@class').get()
        if 'has-img'  in type_review:
           image_link = rev.xpath('./div/div[1]/img/@src').get()
           image_link = image_link[2:]
           image_link = 'https://' + image_link


        
        # xử lý thời gian
        date = int(rev.css('div.main > div > div.block.time::attr(data-time)').get())
        date = date/1000
        dt = datetime.datetime.fromtimestamp(date)
        formatted_date = dt.strftime("%d/%m/%Y")

        # số sao
        star = rev.css('div.main > div > div.block.stars::attr(aria-label)').get()
        star = star.split()[0]
        # star = int(star)


        display_name = rev.css('div.main > div > div.block.title::text').get()
        date = formatted_date
        review_score = star
        product_id = response.meta['product_id']
        email = 'review@abera.us'
        order_id = ''
        review_content = rev.css('div.main > div > div:nth-child(5) > div::text').get()
        media = image_link

        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([review_content, review_score, date, product_id, display_name,email, order_id , media])
            # writer.writerow([test, test2])

        # yield None
    

