1. Cài đặt Python
2. Mở terminal và chạy lệnh 
    `pip install scrapy`
3. Vào thư mục dataset, vào file urls.csv và dán các url cần cào (mỗi dòng một url, giữ header)
4. Mở terminal tại thư mục gốc và chạy các lệnh sau để bắt đầu cào dữ liệu
   4.1 `cd loox_crawler` : Đường dẫn lúc này `~/loox_crawler/loox_crawler/`
   4.2 `scrapy crawl review_crawler`
5. Dữ liệu cào được nằm trong thư mục dataset