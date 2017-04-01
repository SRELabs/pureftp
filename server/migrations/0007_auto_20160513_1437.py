# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0006_hostname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hostname',
            old_name='server_namenew',
            new_name='server_bkname',
        ),
        migrations.RemoveField(
            model_name='hostname',
            name='server_nameold',
        ),
        migrations.AddField(
            model_name='hostname',
            name='server_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
