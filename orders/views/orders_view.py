from django.http import HttpResponse
from django.views import View
from orders.models import Order, Customer, Product, OrderProducts
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
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
        pass
            