from django.contrib import admin

from ping.models import Server, ServerPath


@admin.register(Server)
class ServerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'port', 'title']


@admin.register(ServerPath)
class ServerPathModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'server', 'path', 'status', 'last_ping_at', 'load_time',]
