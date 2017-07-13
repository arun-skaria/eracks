from django.db import connection
from django.conf import settings
from django.db.utils import ProgrammingError

trace = 0


def get_next_id():
    cursor = connection.cursor()
    cursor.execute("select nextval('ids')")
    row = cursor.fetchone()
    return row [0]


# Deprecate legacy single-seq idea from 2001:

ids_present = False
ids_present_set = False

def check_ids_sequence_present():
  global ids_present_set, ids_present

  if ids_present_set:
    return ids_present

  try:
    cursor = connection.cursor()
    cursor.execute("select start_value from ids;")
    row = cursor.fetchone()
    if trace: print row [0]
    ids_present = True
    ids_present_set = True
    return True
  except ProgrammingError, e:
    if trace: print e
    ids_present = False
    ids_present_set = True
    return False

#from django.db.models.signals import pre_save

if settings.TESTING or settings.NODB_COMMAND or not check_ids_sequence_present():
  def presave (sender=None, instance=None, **kw):
    pass
else:
  def presave (sender=None, instance=None, **kw):
    if trace: print 'PRESAVE:', sender, instance, instance.id

    if instance and not instance.id:
        instance.id = get_next_id()

    if trace: print 'PRESAVE RESULT:', instance.id

#pre_save.connect (presave, sender=ProductOption)
