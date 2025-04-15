from django.views import View
from django.shortcuts import render, redirect
from store.models.product import Product
from store.models.orders import Order
from store.models.customer import Customer

class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        return render(request, 'orders.html', {'orders' : orders})
