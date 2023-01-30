from scrapy.exceptions import DropItem

from ping.parser.items import ServerPathItem


class ServerPathPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, ServerPathItem):
            item.save()
            raise DropItem('Stored')
        else:
            return item
