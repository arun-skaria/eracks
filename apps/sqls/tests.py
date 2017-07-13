''' Tests for sqls app - do_sql, do_sql_insert

Org: This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application:

from django.test import TestCase

from django.test import Client
from django.contrib.auth.models import User, Group

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}
'''

from django.test import TransactionTestCase, Client
from django.contrib.auth.models import User, Group
#from django.db import transaction

trace = 0

class ViewsTests (TransactionTestCase):
    fixtures = ['catax.yaml']

    def setUp(self):
        if trace: print 'STARTING SQLS TEST:'
        #with transaction.atomic():
        user1 = User.objects.create_superuser (username="admin_eracks1", email="admin_eracks1@eracks.com", password="admin_eracks1")

    def test_do_sql(self):
        client    = Client()
        response1 = self.client.login (username='admin_eracks1', password='admin_eracks1')
        response  = self.client.post ('/admin/do_sql/', {'sql': 'SELECT * FROM catax;'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        if trace: print response.content
        self.assertEqual (response.status_code, 200)

    def test_do_sql_insert(self):
        client     = Client()
        response1  = self.client.login (username='admin_eracks1', password='admin_eracks1')
        query_post = '''INSERT INTO catax (name,county,tax,cities,count,created,updated) VALUES (\"dfdffsp\",\"iagnaiada\",8.5,\"kgadadaad\",5,\"2015-01-01 12:01AM\",\"2015-01-02 12:01AM\");'''
        response   = self.client.post ('/admin/do_sql/', {'sql': query_post,'updates':'true'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        if trace: print response.content
        self.assertEqual(response.status_code, 200)
