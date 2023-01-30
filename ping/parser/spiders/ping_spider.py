from datetime import timedelta

import scrapy
from django.utils.timezone import localtime
from scrapy.http import Response

from ping.models import ServerPath


class PingSpider(scrapy.Spider):
    name = 'PingSpider'

    def start_requests(self):
        for x in ServerPath.objects.all():
            yield scrapy.Request(
                url=x.url,
                method='HEAD',
                cb_kwargs={
                    'server_path': x,
                }
            )

    def parse(self, response: Response, **kwargs):
        path_obj = kwargs['server_path']
        if path_obj:
            path_obj: ServerPath
            path_obj.status = response.status
            path_obj.last_ping_at = localtime()
            path_obj.load_time = timedelta(seconds=response.meta.get('download_latency') or 0)
            path_obj.save()
