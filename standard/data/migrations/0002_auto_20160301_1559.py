# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.CharField(max_length=30)),
                ('y', models.CharField(max_length=30)),
                ('real_x', models.CharField(max_length=30)),
                ('real_y', models.CharField(max_length=30)),
                ('bssid_team', models.CharField(max_length=30)),
                ('train_num', models.CharField(max_length=30)),
                ('test_num', models.CharField(max_length=30)),
                ('createtime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='StandardData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rssi1', models.CharField(max_length=10)),
                ('rssi2', models.CharField(max_length=10)),
                ('rssi3', models.CharField(max_length=10)),
                ('rssi4', models.CharField(max_length=10)),
                ('x', models.CharField(max_length=30)),
                ('y', models.CharField(max_length=30)),
                ('bssid1', models.CharField(max_length=30)),
                ('bssid2', models.CharField(max_length=30)),
                ('bssid3', models.CharField(max_length=30)),
                ('bssid4', models.CharField(max_length=30)),
                ('team', models.CharField(max_length=30)),
                ('createtime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'standard_data',
            },
        ),
        migrations.DeleteModel(
            name='StardardData',
        ),
    ]
