# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20161120_2339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ipaddress',
            name='which_activity',
        ),
        migrations.AddField(
            model_name='ipaddress',
            name='activity',
            field=models.CharField(blank=True, max_length=100, null=True, help_text=b'activities to log IP-ADDRESS', choices=[(b'Sign-in', b'Sign-in'), (b'Sign-up', b'Sign-up'), (b'Place-an-order', b'Place-an-order'), (b'Request-a-quote', b'Request-a-quote'), (b'Contact-us', b'Contact-us'), (b'Subscribe', b'Subscribe')]),
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
    ]
