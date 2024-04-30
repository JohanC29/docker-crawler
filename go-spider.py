from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from mycrawler.spiders.urbaniaSpider import UrbaniaSpider

process = CrawlerProcess(get_project_settings())
process.crawl(UrbaniaSpider)
process.start()
