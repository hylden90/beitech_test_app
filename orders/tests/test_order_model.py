from django.test import TestCase

from orders.models import Order, Customer, Product, OrderProducts

class OrderModelTests(TestCase):

    def test_when_providing_order_with_not_allowed_products_for_customer_raise_value_error(self):
        
        new_customer = Customer(name='Mike', email='mike@mi.ke')
        new_customer.save()
        milk = Product(name='Milk', price=10)
        milk.save()
        egg = Product(name='Egg', price=3)
        egg.save()
        cheese = Product(name='Cheese', price=8)
        cheese.save()
        
        #Mike can buy milk and cheese
        new_customer.allowed_products.add(milk)
        new_customer.allowed_products.add(cheese)

        #Mike wants to buy milk and two eggs!
        invalid_order = Order()
        invalid_order.customer = new_customer
        invalid_order.save()
        #This is ok!
        OrderProducts.objects.create(order = invalid_order, product = milk, quantity=1)

        #Sorry Mike, you can't buy eggs!
        self.assertRaises(ValueError, OrderProducts.objects.create, order = invalid_order, product = egg, quantity = 2)

    def test_when_providing_orders_with_allowed_products_for_customer_process_successfully(self):
        
        new_customer = Customer(name='Mike', email='mike@mi.ke')
        new_customer.save()
        milk = Product(name='Milk', price=10)
        milk.save()
        egg = Product(name='Egg', price=3)
        egg.save()
        cheese = Product(name='Cheese', price=8)
        cheese.save()
        
        #Mike can buy milk and cheese
        new_customer.allowed_products.add(milk)
        new_customer.allowed_products.add(cheese)

        #Mike wants to buy milk.
        new_order = Order()
        new_order.customer = new_customer
        new_order.save()

        #Mike gets his product because is available for him.
        OrderProducts.objects.create(order = new_order, product = milk, quantity=1)