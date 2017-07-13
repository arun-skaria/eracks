# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20161117_0305'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
