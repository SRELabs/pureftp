# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0007_auto_20160513_1437'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hostname',
            old_name='server_bkname',
            new_name='server_old',
        ),
    ]
