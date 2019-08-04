from django.db import models
from .product import Product

class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    allowed_products = models.ManyToManyField(Product, db_table='orders_products_availability')

    def __str__(self):
        return self.name