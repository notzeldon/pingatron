import urllib.parse
from typing import Union

import scrapy
from django.core.management import CommandError
from scrapy.http import Response

from ping.parser.items import ServerPathItem
from ping.models import Server


class ParseSiteSpider(scrapy.Spider):
    name = 'ParseSiteSpider'
    download_delay = 0.25

    def __init__(self,  site_or_server: Union[str, Server] = None, *args, **kwargs):
        if isinstance(site_or_server, str):
            try:
                server = Server.objects.filter(host=site_or_server).get()
            except Server.DoesNotExist:
                raise CommandError(f'Server with host "{site_or_server}" not found')
        elif isinstance(site_or_server, Server):
            server = site_or_server
        else:
            raise CommandError('Host or server object required')

        self.server: Server = server
        self.server_parts = urllib.parse.urlsplit(server.url)
        super().__init__(*args, **kwargs)

    def start_requests(self):
        yield scrapy.Request(
            url=self.server.url,
        )

    def parse(self, response: Response, **kwargs):
        item = ServerPathItem(server=self.server)
        item['url'] = response.url
        yield item

        links = response.css('a[href]')
        for true_link in filter(
                lambda x: x.attrib['href'].startswith('/') or x.attrib['href'].startswith('http'), links
        ):
            href = true_link.attrib['href']
            if '/media/' in href:
                continue
            href = href.strip()
            if href.startswith('//'):
                href = f'http:{href}'
            parsed_url = urllib.parse.urlsplit(href)

            if not parsed_url.netloc:
                parsed_url = parsed_url._replace(scheme=self.server_parts.scheme, netloc=self.server_parts.netloc)
            elif self.server_parts.netloc != parsed_url.netloc:
                continue

            next_url = urllib.parse.urlunsplit(parsed_url)
            yield scrapy.Request(
                url=next_url,
            )


