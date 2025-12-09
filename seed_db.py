#!/usr/bin/env python3
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")
django.setup()

from crm.models import Customer, Product
from decimal import Decimal

def seed():
    products = [
        {"name": "Laptop", "price": Decimal("999.99"), "stock": 10},
        {"name": "Phone", "price": Decimal("499.50"), "stock": 25},
        {"name": "Headphones", "price": Decimal("79.90"), "stock": 100},
    ]
    for p in products:
        obj, created = Product.objects.get_or_create(name=p["name"], defaults={"price":p["price"], "stock":p["stock"]})
        print("Product:", obj, "created:", created)

    customers = [
        {"name": "Alice", "email": "alice@example.com", "phone": "+1234567890"},
        {"name": "Bob", "email": "bob@example.com", "phone": "123-456-7890"},
    ]
    for c in customers:
        obj, created = Customer.objects.get_or_create(email=c["email"], defaults={"name":c["name"], "phone":c["phone"]})
        print("Customer:", obj, "created:", created)

if __name__ == "__main__":
    seed()
