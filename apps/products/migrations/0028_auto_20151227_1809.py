# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_auto_20151121_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option2',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('products.option',),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(db_column=b'categoryid', to='products.Categories', help_text=b'Primary Category for this product.'),
        ),
    ]
