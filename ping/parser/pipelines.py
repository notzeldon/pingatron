import urllib.parse

from scrapy.exceptions import DropItem

from ping.models import ServerPath
from ping.parser.items import ServerPathItem


class ServerPathPipeline(object):

    STORAGE = {}
    def store(self, url, server_id):
        self.STORAGE[url] = server_id
        if len(self.STORAGE) >= 1000:
            self.save()

    def save(self):
        qs = ServerPath.objects.filter(
            url__in=self.STORAGE.keys(),
            server_id__in=set(self.STORAGE.values())
        )

        exists_data = set(qs.values_list('url', flat=True))
        need_create = set(self.STORAGE) - set(exists_data)

        new_objects = []
        for x in need_create:
            obj = ServerPath(
                url=x, server_id=self.STORAGE.get(x),
            )
            new_objects.append(obj)

        ServerPath.objects.bulk_create(new_objects)


    def process_item(self, item, spider):
        if isinstance(item, ServerPathItem):
            server = item['server']
            parts = urllib.parse.urlsplit(item['url'])
            url = parts.path
            self.store(url, server.id)

        #     raise DropItem('Stored')
        # else:
        #     return item

    def close_spider(self, spider):
        self.save()
