from django.shortcuts import render
from rest_framework import viewsets

from payment_app.models import Payment, PaymentItem
from payment_app.serializers import PaymentSerializer, PaymentItemSerializer


class PaymentView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentItemView(viewsets.ModelViewSet):
    queryset = PaymentItem.objects.all()
    serializer_class = PaymentItemSerializer


