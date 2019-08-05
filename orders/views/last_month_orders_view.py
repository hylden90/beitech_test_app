from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from datetime import datetime, timezone, timedelta

from orders.models import Order, OrderProducts, Product

class LastMonthOrdersView(View):
    model = Order

    def get(self, request):
        try:
            customer_id = request.GET['customer']
            orders = Order.objects.filter(customer_id=request.GET['customer'],
                                          creation_date__lte=datetime.now(timezone.utc),
                                          creation_date__gte=datetime.now(timezone.utc)-timedelta(days=30))
            return render(request, 'orders/orders.html', {'orders':orders, 'customer':customer_id})
        except KeyError as e:
            return HttpResponse("Missing customer argument", status=400)
