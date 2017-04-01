# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_auto_20160504_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='server_createtime',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='server_finishtime',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
