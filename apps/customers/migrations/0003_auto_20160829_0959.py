# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_auto_20150515_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(related_name='customer', verbose_name=b'user', to=settings.AUTH_USER_MODEL),
        ),
    ]
