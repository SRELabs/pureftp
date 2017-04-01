# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('server_id', models.AutoField(serialize=False, primary_key=True)),
                ('server_name', models.CharField(max_length=50)),
                ('server_ip', models.CharField(max_length=18)),
                ('server_description', models.CharField(max_length=255)),
                ('server_diskinfo', models.CharField(max_length=255, null=True, blank=True)),
                ('server_cpuinfo', models.CharField(max_length=50, null=True, blank=True)),
                ('server_memoryinfo', models.CharField(max_length=10, null=True, blank=True)),
                ('server_internetip', models.CharField(max_length=18, null=True, blank=True)),
                ('server_status', models.IntegerField(default=0)),
                ('server_assign_status', models.IntegerField(default=0, choices=[(3, b'\xe5\xb7\xb2\xe6\x8b\x92\xe7\xbb\x9d'), (1, b'\xe5\x8f\xaf\xe5\x88\x86\xe9\x85\x8d'), (4, b'\xe5\xb7\xb2\xe5\x88\x86\xe9\x85\x8d'), (0, b'\xe4\xb8\x8d\xe5\x8f\xaf\xe5\x88\x86\xe9\x85\x8d'), (2, b'\xe5\xb7\xb2\xe6\x92\xa4\xe9\x94\x80')])),
            ],
        ),
        migrations.CreateModel(
            name='ServerAssign',
            fields=[
                ('assign_id', models.AutoField(serialize=False, primary_key=True)),
                ('assign_status', models.IntegerField(default=1, choices=[(1, b'\xe5\xbe\x85\xe5\x88\x86\xe9\x85\x8d'), (3, b'\xe5\xb7\xb2\xe6\x8b\x92\xe7\xbb\x9d'), (4, b'\xe5\xb7\xb2\xe5\x88\x86\xe9\x85\x8d'), (0, b'\xe4\xb8\x8d\xe5\x8f\xaf\xe5\x88\x86\xe9\x85\x8d'), (2, b'\xe5\xb7\xb2\xe6\x92\xa4\xe9\x94\x80')])),
                ('assign_config', models.CharField(max_length=255)),
                ('assign_description', models.CharField(max_length=50)),
                ('assign_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServerLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('parent_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='server',
            name='server_location',
            field=models.ForeignKey(to='server.ServerLocation', on_delete=b'PROTECT'),
        ),
        migrations.AddField(
            model_name='server',
            name='server_uid',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
