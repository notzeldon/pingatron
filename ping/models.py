import requests
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _
from requests import ReadTimeout


class Server(models.Model):
    class Meta:
        verbose_name = _('server')
        verbose_name_plural = _('servers')

        ordering = ['title', 'host']

    title = models.CharField(
        _('title'),
        max_length=255,
        blank=True,
        default='',
    )

    host = models.URLField(
        _('host'),
        max_length=255,
        db_index=True,
    )

    port = models.PositiveIntegerField(
        _('port'),
        blank=True,
        null=True,
    )

    @property
    def url(self):
        tmp = f'{self.host}'
        if self.port:
            tmp = f'{tmp}:{self.port}'
        return tmp

    def get_absolute_url(self):
        return self.url

    def __str__(self):
        return self.title or self.url


class ServerPath(models.Model):
    class Meta:
        verbose_name = _('server path')
        verbose_name_plural = _('server paths')

        ordering = ['server', 'path', ]
        unique_together = ['server', 'path', ]

    server = models.ForeignKey(
        verbose_name=Server._meta.verbose_name,
        to=Server,
        on_delete=models.CASCADE,
        related_name='paths',
    )

    title = models.CharField(
        _('title'),
        max_length=255,
        blank=True,
        default='',
    )

    path = models.CharField(
        _('relative path'),
        max_length=1023,
        db_index=True,
        default='/',
        blank=True,
    )

    status = models.IntegerField(
        _('status'),
        default=0,
        db_index=True,
        editable=False,
    )

    max_timeout = models.PositiveIntegerField(
        _('max timeout'),
        default=0,
    )

    last_ping_at = models.DateTimeField(
        blank=True,
        null=True,
        editable=False,
    )

    load_time = models.DurationField(
        blank=True,
        null=True,
        editable=False,
    )

    @property
    def url(self):
        return f'{self.server.url}{self.path}'

    def ping(self):
        update_fields = dict(
            status=0,
            last_ping_at=localtime(),
        )
        request_kwargs = dict()
        if self.max_timeout:
            request_kwargs['timeout'] = self.max_timeout
        try:
            response = requests.head(self.url, **request_kwargs)
        except ReadTimeout as e:
            update_fields.update(
                status=-1,
            )
        else:
            update_fields.update(
                status=response.status_code,
                load_time=response.elapsed,
            )
        self._meta.model.objects.filter(pk=self.pk).update(**update_fields)
        return update_fields['status']

    def __str__(self):
        return self.title or self.url


@receiver(post_save, sender=Server, dispatch_uid='ping.models.Server.post_save')
def ping_models_server_post_save(sender, instance: Server, **kwargs):
    if not instance.paths.exists():
        ServerPath(
            server=instance,
        ).save()


@receiver(post_save, sender=ServerPath, dispatch_uid='ping.models.ServerPath.post_save')
def ping_models_server_path_post_save(sender, instance: ServerPath, **kwargs):
    if instance.pk:
        instance.ping()
