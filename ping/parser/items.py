import urllib.parse

import scrapy

from ping.models import Server, ServerPath


class ServerPathItem(scrapy.Item):
    server = scrapy.Field()
    url = scrapy.Field()

    def __init__(self, server: Server, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['server'] = server

    def save(self):
        pass
        # server = self['server']
        # url = self['url']
        #
        # parts = urllib.parse.urlsplit(url)
        # qs = ServerPath.objects.filter(server=server, path=parts.path)
        # if not qs.exists():
        #     server_path = ServerPath(server=server, path=parts.path)
        #     server_path.save()
