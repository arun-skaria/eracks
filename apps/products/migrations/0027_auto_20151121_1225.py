# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoryimage',
            options={'ordering': ['sortorder']},
        ),
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ['sortorder']},
        ),
    ]
