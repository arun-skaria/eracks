# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_activity_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_name',
            field=models.CharField(help_text=b'-Which all activities to log IP-ADDRESS', max_length=100, choices=[(b'Sign-in', b'Sign-in'), (b'Sign-up', b'Sign-up'), (b'Place-an-order', b'Place-an-order'), (b'Request-a-quote', b'Request-a-quote'), (b'Contact-us', b'Contact-us'), (b'Subscribe', b'Subscribe')]),
        ),
    ]
