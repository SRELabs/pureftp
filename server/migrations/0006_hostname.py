# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_auto_20160504_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hostname',
            fields=[
                ('hn_id', models.AutoField(serialize=False, primary_key=True)),
                ('server_id', models.IntegerField(default=0)),
                ('server_namenew', models.CharField(max_length=50)),
                ('server_ip', models.CharField(max_length=18)),
                ('hn_user_name', models.CharField(max_length=50)),
                ('hn_msg', models.TextField(max_length=4096)),
                ('server_flag', models.IntegerField(default=0)),
                ('server_flag_status', models.IntegerField(default=0, choices=[(3, b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x88\x90\xe5\x8a\x9f'), (1, b'\xe4\xbf\xae\xe6\x94\xb9\xe4\xb8\xad'), (2, b'\xe4\xbf\xae\xe6\x94\xb9\xe5\xa4\xb1\xe8\xb4\xa5'), (0, b'\xe5\xbe\x85\xe4\xbf\xae\xe6\x94\xb9')])),
                ('server_nameold', models.CharField(max_length=50, null=True, blank=True)),
                ('server_createtime', models.DateTimeField(auto_now=True, null=True)),
                ('server_finishtime', models.DateTimeField(null=True, blank=True)),
            ],
        ),
    ]
