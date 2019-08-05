from django.test import TestCase, Client
from django.urls import reverse
from django.test.utils import setup_test_environment
import json

from orders.models import Order, Customer, Product, OrderProducts

class OrdersViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.path = '/orders/'
        super().setUp()
    
    def test_when_invalid_json_on_post_return_400(self):
        invalid_json = '{"customer":1'
        response = self.client.post(self.path, invalid_json, 'application/json')
        self.assertEqual(400, response.status_code)

    def test_when_no_customer_provided_return_400(self):
        no_customer_input = {"products":[1,2]}
        response = self.client.post(self.path, json.dumps(no_customer_input), 'application/json')
        self.assertEqual(400, response.status_code)

    def test_when_no_products_provided_return_400(self):
        no_products_input = {"customer":1}
        response = self.client.post(self.path, json.dumps(no_products_input), 'application/json')
        self.assertEqual(400, response.status_code)

    def test_when_any_of_attributes_is_invalid_type_return_400(self):
        input = {"customer":1, "products":1}
        response = self.client.post(self.path, json.dumps(input), 'application/json')
        self.assertEqual(400, response.status_code)

    def test_when_customer_does_not_exist_return_400(self):
        #No entities created so far, so...
        input = {"customer":1, "products":[1, 2]}
        response = self.client.post(self.path, json.dumps(input), 'application/json')
        self.assertEqual(400, response.status_code)

    def test_when_any_product_does_not_exist_return_400(self):
        #Only the customer is created in the system.
        mike = Customer.objects.create(name='mike', email='mike@mi.ke')
        input = {"customer":mike.id, "products":[1, 2]}
        response = self.client.post(self.path, json.dumps(input), 'application/json')
        self.assertEqual(400, response.status_code)

    def test_when_any_product_is_not_registered_for_customer_return_400(self):
        mike = Customer.objects.create(name='mike', email='mike@mi.ke')
        #Create products
        milk = Product.objects.create(name='Milk', price=10)
        cheese = Product.objects.create(name='Cheese', price=8)
        #Relate Milk to Mike, but not Cheese
        mike.allowed_products.add(milk)
        input = {"customer":mike.id, "products":[mike.id, cheese.id]}
        response = self.client.post(self.path, json.dumps(input), 'application/json')
        self.assertEqual(400, response.status_code)

    def test_when_products_are_related_to_customer_return_201(self):
        mike = Customer.objects.create(name='mike', email='mike@mi.ke')
        #Create products
        milk = Product.objects.create(name='Milk', price=10)
        cheese = Product.objects.create(name='Cheese', price=8)
        #Relate Milk and Cheese to Mike
        mike.allowed_products.add(milk)
        mike.allowed_products.add(cheese)
        input = {"customer":mike.id, "products":[mike.id, cheese.id]}
        response = self.client.post(self.path, json.dumps(input), 'application/json')
        self.assertEqual(201, response.status_code)