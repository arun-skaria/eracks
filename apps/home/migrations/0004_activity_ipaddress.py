# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_lengthen_auth_user_username_20160927'),
        ('home', '0003_auto_20151107_0928'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_name', models.CharField(help_text=b'- Which all activities to save IP-ADDRESS', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='IpAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.GenericIPAddressField(null=True, blank=True)),
                ('comments', models.TextField(null=True, blank=True)),
                ('customer', models.ForeignKey(blank=True, to='customers.Customer', null=True)),
                ('which_activity', models.ForeignKey(blank=True, to='home.Activity', null=True)),
            ],
        ),
    ]
