# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_server_server_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='server_flag_status',
            field=models.IntegerField(default=0, choices=[(3, b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x88\x90\xe5\x8a\x9f'), (1, b'\xe4\xbf\xae\xe6\x94\xb9\xe4\xb8\xad'), (2, b'\xe4\xbf\xae\xe6\x94\xb9\xe5\xa4\xb1\xe8\xb4\xa5'), (0, b'\xe5\xbe\x85\xe4\xbf\xae\xe6\x94\xb9')]),
        ),
        migrations.AddField(
            model_name='server',
            name='server_nameold',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
