# Generated by Django 4.1.5 on 2023-01-11 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ping', '0002_remove_server_scheme'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverpath',
            name='load_time',
            field=models.DurationField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='serverpath',
            name='max_timeout',
            field=models.PositiveIntegerField(default=0, verbose_name='max timeout'),
        ),
        migrations.AlterField(
            model_name='serverpath',
            name='status',
            field=models.IntegerField(db_index=True, default=0, editable=False, verbose_name='status'),
        ),
    ]
