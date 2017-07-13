# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0028_auto_20151227_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choicecategory',
            field=models.ForeignKey(default=products.models.get_misc_choice_category, verbose_name=b'category', to='products.ChoiceCategory'),
        ),
        migrations.AlterField(
            model_name='prodopt',
            name='defaultchoice',
            field=models.ForeignKey(db_column=b'defaultchoiceid', default=products.models.get_none_choice, to='products.Choice', help_text=b"Default choice from list of option-choices or legacy POCs - <b><span style='color:red'>SAVE TWICE to set this correctly</span></b>, otherwise fault will occur on ajax product update!"),
        ),
    ]
