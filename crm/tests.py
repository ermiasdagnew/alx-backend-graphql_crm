from django.test import TestCase
from .models import Customer, Product, Order

class SmokeTests(TestCase):
    def test_create_customer(self):
        c = Customer.objects.create(name="T", email="t@example.com")
        self.assertEqual(Customer.objects.count(), 1)
