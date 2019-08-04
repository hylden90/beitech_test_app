from django.db import models
from .customer import Customer
from .product import Product

class Order(models.Model):
    total_price = models.IntegerField(default=0)
    creation_date = models.DateTimeField()
    customer_id = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    products = models.ManyToManyField(Product)