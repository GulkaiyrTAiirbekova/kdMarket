from rest_framework import serializers
from .models import Order
from .models import OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem ##закзанный товар
        fields = '__all__'


