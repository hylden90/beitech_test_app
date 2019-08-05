from django.http import HttpResponse
from django.views import View
from orders.models import Order, Customer, Product, OrderProducts
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime, timezone, timedelta
import json


@method_decorator(csrf_exempt, name='dispatch')
class OrdersView(View):

    def post(self, request, *args, **kwargs):

        try:
            data = json.loads(request.body)
            customer = Customer.objects.get(pk=data['customer'])
            new_order = Order.objects.create(customer=customer)
            for product_id in data['products']:
                product = Product.objects.get(pk=product_id)
                try:
                    OrderProducts.objects.create(order=new_order, product=product, quantity=1)
                except (Product.DoesNotExist, ValueError) as e:
                    new_order.delete()
                    raise e
            response = {'Result':'Order created', 'orderId':new_order.id, 'totalPrice':new_order.total_price}
            return HttpResponse(json.dumps(response), status=201)

        except json.decoder.JSONDecodeError as e:
            response = {'Result':'Error', 'Description':'Input is not a valid JSON.'}
            return HttpResponse(json.dumps(response), status=400)
        except (KeyError, TypeError) as e:
            response = {'Result':'Error', 'Description':'Input is not a valid order.'}
            return HttpResponse(json.dumps(response), status=400)
        except Customer.DoesNotExist as e:
            response = {'Result':'Error', 'Description':'Provided customer does not exist. Unable to create order.'}
            return HttpResponse(json.dumps(response), status=400)
        except Product.DoesNotExist as e:
            response = {'Result':'Error', 
                        'Description':'Some of the provided products do not exist. Unable to create order.'}
            return HttpResponse(json.dumps(response), status=400)
        except ValueError as e:
            response = {'Result':'Error', 'Description': str(e)}
            return HttpResponse(json.dumps(response), status=400)
               

    def get(self, request):
        try:
            self.query_data = request.GET
            self.customer_id = self.query_data['customer']
            self.from_date = datetime.strptime(self.query_data['from'], '%Y-%m-%d')
            self.from_date -= timedelta(days=1)
            self.to_date = datetime.strptime(self.query_data['to'], '%Y-%m-%d')
            self.to_date += timedelta(days=1)
            self.orders = Order.objects.filter(customer_id=self.query_data['customer'],
                                          creation_date__lte=self.to_date,
                                          creation_date__gte=self.from_date)
            response = []

            for order in self.orders:
                response.append({"orderId":order.id, 
                                 "customerId":order.customer_id, 
                                 "totalPrice":order.total_price,
                                 "products":[]})
                for product in order.products.all():
                    order_product = OrderProducts.objects.get(order_id=order.id, product_id=product.id)
                    response[len(response)-1]['products'].append({"name":product.name, "quantity":order_product.quantity})


            return HttpResponse(json.dumps(response), status=200)
        except KeyError as e:
            response = {"Response":"Error", "Description":"customer, from and to arguments are required at query string"}
            return HttpResponse(json.dumps(response), status=400)
            