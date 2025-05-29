from django.shortcuts import render
from rest_framework import viewsets

from orders_app.models import Order, OrderItem
from orders_app.serializers import OrderSerializer, OrderItemSerializer


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemView(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


