# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings

from django.db import migrations, models

'''
from django.db.migrations.operations.base import Operation

import django.core.validators


class LengthenUsername (Operation):

    # If this is False, it means that this operation will be ignored by
    # sqlmigrate; if true, it will be run and the SQL collected for its output.
    reduces_to_sql = False

    # If this is False, Django will refuse to reverse past this operation.
    reversible = False

    def __init__(self, arg1, arg2):
        # Operations are usually instantiated with arguments in migration
        # files. Store the values of them on self for later use.
        pass

    def state_forwards(self, app_label, state):
        # The Operation should take the 'state' parameter (an instance of
        # django.db.migrations.state.ProjectState) and mutate it to match
        # any schema changes that have occurred.
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        # The Operation should use schema_editor to apply any changes it
        # wants to make to the database.
        schema_editor.execute ('ALTER TABLE "auth_user" ALTER COLUMN "username" TYPE varchar(128);')

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        # If reversible is True, this is called when the operation is reversed.
        pass

    def describe(self):
        # This is used to describe what the operation does in console output.
        return "Lengthen auth.user.username to 128 chars"
'''


if settings.TESTING:
  sql = migrations.RunSQL.noop
else:
  sql = 'ALTER TABLE "auth_user" ALTER COLUMN "username" TYPE varchar(128);'

class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20160829_0959'),
    ]

    operations = [
        migrations.RunSQL (sql, reverse_sql=migrations.RunSQL.noop)
        # Nope, takes 3 parms:
        #LengthenUsername(),

        # Nope, this doesn't work, assumes only in current app:
        #migrations.AlterField (
        #    model_name='auth.user',
        #    name='username',
        #    field=models.CharField(help_text='Required. 128 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=128, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')]),
        #    preserve_default=True,
        #),
    ]
