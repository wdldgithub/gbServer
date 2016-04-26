# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingRawData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ssid', models.CharField(max_length=30)),
                ('bssid', models.CharField(max_length=30)),
                ('rssi', models.CharField(max_length=10)),
                ('device_id', models.CharField(max_length=30)),
                ('market_id', models.CharField(max_length=10)),
                ('floor_id', models.CharField(max_length=10)),
                ('x', models.CharField(max_length=30)),
                ('y', models.CharField(max_length=30)),
                ('createtime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'training_raw_data',
            },
        ),
    ]
