# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StardardData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rssi1', models.CharField(max_length=10)),
                ('rssi2', models.CharField(max_length=10)),
                ('rssi3', models.CharField(max_length=10)),
                ('rssi4', models.CharField(max_length=10)),
                ('x', models.CharField(max_length=30)),
                ('y', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'standard_data',
            },
        ),
    ]
