from django.test import TestCase

from orders.models import Order, Customer, Product

class OrderModelTests(TestCase):

    def test_when_try_create_order_with_no_allowed_products_for_customer_raise_value_error(self):
        
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
        invalid_order.products.add(milk)
        invalid_order.products.add(egg)
        invalid_order.products.add(egg)

        #Sorry Mike, you can't buy some of the products!
        self.assertRaises(ValueError, invalid_order.save)

    def test_when_try_create_order_with_allowed_products_for_customer_process_successfully(self):
        
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
        invalid_order = Order()
        invalid_order.customer = new_customer
        invalid_order.save()

        #Mike gets his product because is available for him.
        invalid_order.products.add(milk)