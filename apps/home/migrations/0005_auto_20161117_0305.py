# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_activity_ipaddress'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name': 'Activity', 'verbose_name_plural': 'Activities'},
        ),
        migrations.AlterModelOptions(
            name='ipaddress',
            options={'verbose_name': 'IpAddress', 'verbose_name_plural': 'IpAddresses'},
        ),
        migrations.AddField(
            model_name='activity',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='ipaddress',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='activity_name',
            field=models.CharField(help_text=b'-Which all activities to save IP-ADDRESS', max_length=100),
        ),
    ]
