from django.core.management import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from ping.models import Server
from ping.parser.spiders.parse_spider import ParseSiteSpider
from ping.parser.spiders.ping_spider import PingSpider


class Command(BaseCommand):

    def  add_arguments(self, parser):
        parser.add_argument(
            '--host',
            action='store',
            help='''Host url'''
        )
        parser.add_argument(
            '--server-id', '-si',
            action='store',
            type=int,
            help='''Server id from databse'''
        )

    def handle(self, *args, **options):
        server_id = options.get('server_id')
        server = None
        if server_id:
            server = Server.objects.filter(pk=server_id).first()
        host = options.get('host')

        config = get_project_settings()
        process = CrawlerProcess(settings=config)

        process.crawl(ParseSiteSpider, site_or_server=host or server)
        process.start()
