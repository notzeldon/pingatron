from django.core.management import BaseCommand
from scrapy.crawler import CrawlerProcess

from ping.parser.spiders.ping_spider import PingSpider


class Command(BaseCommand):

    def handle(self, *args, **options):
        process = CrawlerProcess()

        process.crawl(PingSpider)
        process.start()
