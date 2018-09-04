from scrapy import cmdline

cmdline.execute('scrapy crawl douban_spider'.split())
# scrapy crawl douban_spider -o douban250.json
# scrapy crawl douban_spider -o douban250.csv