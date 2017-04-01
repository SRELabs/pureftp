# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='server_assign_status',
            field=models.IntegerField(default=0, choices=[(3, b'\xe5\xb7\xb2\xe6\x8b\x92\xe7\xbb\x9d'), (1, b'\xe5\x8f\xaf\xe5\x88\x86\xe9\x85\x8d'), (4, b'\xe5\xb7\xb2\xe5\x88\x86\xe9\x85\x8d'), (0, b'\xe4\xb8\x8d\xe5\x8f\xaf\xe5\x88\x86\xe9\x85\x8d'), (2, b'\xe5\xb7\xb2\xe6\x92\xa4\xe9\x94\x80')]),
        ),
    ]
