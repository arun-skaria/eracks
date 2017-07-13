# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0008_auto_20151227_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='quote_number',
            field=models.CharField(help_text=b'eRacks quote id - letters/numbers/underscore/dashes ok, no spaces', max_length=20),
        ),
    ]
