from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .customer import Customer
from .product import Product

class Order(models.Model):
    total_price = models.IntegerField(default=0)
    creation_date = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    products = models.ManyToManyField(Product, through='OrderProducts')
    
class OrderProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()

@receiver(pre_save, sender=OrderProducts)
def order_products_save_handler(sender, **kwargs):
    if kwargs['instance'].product not in kwargs['instance'].order.customer.allowed_products.all():
        raise ValueError('Product {} is not available for Customer {}'
                         .format(kwargs['instance'].product, kwargs['instance'].order.customer))