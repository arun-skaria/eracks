# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20150729_1317'),
        ('quotes', '0010_auto_20161103_2232'),
        ('home', '0008_auto_20161121_0045'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipaddress',
            name='order',
            field=models.ForeignKey(blank=True, to='orders.Order', null=True),
        ),
        migrations.AddField(
            model_name='ipaddress',
            name='quote',
            field=models.ForeignKey(blank=True, to='quotes.Quote', null=True),
        ),
    ]
