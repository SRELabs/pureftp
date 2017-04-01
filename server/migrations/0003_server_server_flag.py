# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20160413_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='server_flag',
            field=models.IntegerField(default=0),
        ),
    ]
