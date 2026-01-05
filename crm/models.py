from django.db import models

class Customer(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
