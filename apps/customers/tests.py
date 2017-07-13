"""
These are the tests for the customers app.
These will pass (or not!) when you run "manage.py test".
"""

from django.test import TestCase
from django.contrib.auth.models import User, Group
from customers.models import *
from django.test import Client


class FixturesTest(TestCase):
    fixtures = ['customers-54730.yaml',]  # 'customers-customerimage-53336.yaml',]  # 'users.yaml', 'customers.yaml']

    def test_customers_fixtures(self):
        user1 = User.objects.get(pk=50)
        c = Customer.objects.get(user=user1)
        self.assertTrue(c)


class ViewsTests(TestCase):
    fixtures = ['customers-54730.yaml', 'customers-customerimage-53336.yaml', 'quickpages.yaml']

    def test_save_email(self):
        client = Client()
        response = client.get("/customers/save_email/")
        self.assertEqual(response.status_code, 200)

    def test_save_email_post(self):
        client = Client()
        response = client.post(
            "/customers/save_email/", {'email': 'neweracksuser1@yopmail.com'})
        self.assertIn("Thank you and welcome to eRacks!", response.content)

    def test_emails(self):
        client = Client()
        response1 = client.post(
            "/accounts/login/", {'identification': 'testmailname1', 'password': 'testuser1'}, follow=True)
        response2 = client.post("/customers/emails/", follow=True)
        self.assertEqual(response2.status_code, 200)

    def test_customers(self):
        client = Client()
        response = client.get("/customers/")
        self.assertIn("National Public Radio", response.content)


class CustomerTest(TestCase):
    def setUp(self):
        user1 = User.objects.create (
            username="testuser1",
            email="testuser1@yahoo.com",
            password="testuser1",
          )
        customer1 = Customer.objects.get (user=user1)
        address1 = Address.objects.create (
            customer=customer1,
            address1='street',
            city='texas',
            state='CA',
            zip='556655',
            country='US',
            phone='123456',
            email='testuser1@yahoo.com',
            type='shipping',
          )

    def test_create_user_profile(self):
        user1 = User.objects.get(email="testuser1@yahoo.com")
        customer1 = Customer.objects.get(user=user1)
        self.assertEqual(user1, customer1.user)

    def test_name(self):
        user1 = User.objects.get(email="testuser1@yahoo.com")
        user1.first_name = 'test'
        user1.last_name = 'case'
        user1.save()
        customer1 = Customer.objects.get(user=user1)
        self.assertEqual(customer1.name(), 'test case')

    def test_default_shipping(self):
        user1 = User.objects.get(email="testuser1@yahoo.com")
        customer1 = Customer.objects.get(user=user1)
        address1 = Address.objects.get(customer=customer1)
        self.assertTrue(customer1.default_shipping())

    def test_default_billing(self):
        user1 = User.objects.get(email="testuser1@yahoo.com")
        customer1 = Customer.objects.get(user=user1)
        address1 = Address.objects.get(customer=customer1)
        self.assertFalse(customer1.default_billing())


class AddressTest(TestCase):
    def setUp(self):
        user1 = User.objects.create (
            username="testuser1",
            email="testuser1@yahoo.com",
            password="testuser1",
          )
        customer1 = Customer.objects.get (user=user1)
        address1 = Address.objects.create (
            customer=customer1,
            address1='street',
            city='texas',
            state='CA',
            zip='556655',
            country='US',
            phone='123456',
            email='testuser1@yahoo.com',
            type='shipping',
          )

    def test_is_shipping(self):
        user1 = User.objects.get(email="testuser1@yahoo.com")
        customer1 = Customer.objects.get(user=user1)
        address1 = Address.objects.get(customer=customer1)
        self.assertTrue(address1.is_shipping())

    def test_is_billing(self):
        user1 = User.objects.get(email="testuser1@yahoo.com")
        customer1 = Customer.objects.get(user=user1)
        address1 = Address.objects.get(customer=customer1)
        self.assertFalse(address1.is_billing())
