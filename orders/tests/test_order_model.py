from django.test import TestCase

from orders.models import Order, Customer, Product, OrderProducts

class OrderModelTests(TestCase):

    def setUp(self):
        self.mike = Customer(name='Mike', email='mike@mi.ke')
        self.mike.save()
        self.milk = Product(name='Milk', price=10)
        self.milk.save()
        self.egg = Product(name='Egg', price=3)
        self.egg.save()
        self.cheese = Product(name='Cheese', price=8)
        self.cheese.save()
        return super().setUp()

    def test_when_providing_order_with_not_allowed_products_for_customer_raise_value_error(self):
        
        #Mike can now buy milk and cheese
        self.mike.allowed_products.add(self.milk)
        self.mike.allowed_products.add(self.cheese)

        #Mike wants to buy milk and two eggs!
        invalid_order = Order()
        invalid_order.customer = self.mike
        invalid_order.save()
        #This is ok!
        OrderProducts.objects.create(order = invalid_order, product = self.milk, quantity=1)
        #Sorry Mike, you can't buy eggs!
        self.assertRaises(ValueError, OrderProducts.objects.create, order = invalid_order, product = self.egg, quantity = 2)

    def test_when_providing_orders_with_allowed_products_for_customer_process_successfully(self):
        
        #Mike can now buy milk and cheese
        self.mike.allowed_products.add(self.milk)
        self.mike.allowed_products.add(self.cheese)

        #Mike wants to buy milk.
        new_order = Order()
        new_order.customer = self.mike
        new_order.save()
        #Mike gets his product because is available for him.
        OrderProducts.objects.create(order = new_order, product = self.milk, quantity=1)

    