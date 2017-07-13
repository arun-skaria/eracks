# -*- coding: utf-8 -*-

from django.db import models

class Catax(models.Model):
    name    = models.CharField(max_length=200, unique=True, help_text='County, plus city in parens for rate exceptions')
    county  = models.CharField(max_length=50, help_text="County name only")
    tax     = models.DecimalField (max_digits=5, decimal_places=2, help_text='Total CA Sales Tax rate')
    #city   = models.CharField(max_length=50)
    cities  = models.TextField (blank=True, help_text='Comma-separated list of cities within the county for which this tax rate applies')
    count   = models.IntegerField(help_text='Count of cities, used to determine the need for the city to be added to the county for uniqueness')

    created     = models.DateTimeField (auto_now_add=True)
    updated     = models.DateTimeField (auto_now=True)

    def __unicode__ (self):
        return self.name

    class Meta:
        db_table = u'catax'
        unique_together = ('county','tax')
        verbose_name = 'CA Tax'
        verbose_name_plural = 'CA Taxes'
        ordering=('name',)


#### Set up single-seq tables (org fm legacy eracks db - all db id's in one sequence)

#from apps
import helpers
from django.db.models.signals import pre_save

pre_save.connect (helpers.presave, sender=Catax)

