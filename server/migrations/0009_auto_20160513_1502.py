# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0008_auto_20160513_1444'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hostname',
            old_name='server_old',
            new_name='server_oldname',
        ),
    ]
