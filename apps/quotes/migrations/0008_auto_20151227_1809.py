# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0007_quotelineitem_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quotelineitem',
            options={'ordering': ['-modified']},
        ),
    ]
