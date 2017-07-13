# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catax', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catax',
            name='cities',
            field=models.TextField(help_text=b'Comma-separated list of cities within the county for which this tax rate applies', blank=True),
        ),
        migrations.AlterField(
            model_name='catax',
            name='name',
            field=models.CharField(help_text=b'County, plus city in parens for rate exceptions', unique=True, max_length=200),
        ),
    ]
